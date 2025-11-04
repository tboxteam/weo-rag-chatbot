# REPO: weo-rag-chatbot
# FILE: agent.py
# =========================================
# บทบาทไฟล์นี้ (RAG Agent)
# - "ประกอบ" ระบบตอบคำถามโดยใช้ 2 ส่วน:
#   1) Retrieval (ดึงชิ้นความรู้จริงจาก Qdrant)
#   2) LLM (gemma3:1b via Ollama) ตอบโดยยึดตาม CONTEXT เท่านั้น
# - นโยบาย: ต้องอ้างอิง [p.X] เสมอ ถ้าหลักฐานไม่พอ ให้ปฏิเสธ
#
# หลักการออกแบบพรอมต์ (Prompt) แบบ RAG:
# - ย้ำกติกาว่า "ห้ามเดา" และ "ต้องใส่ citation"
# - ให้ CONTEXT เป็นชิ้น ๆ (C1, C2, ...) เพื่อให้โมเดลใช้ข้อมูลล่าสุดที่ดึงมา
# - ทำให้คำสั่งสั้น ชัด เข้าใจง่าย (LLM เล็ก ๆ ชอบพรอมต์ตรงไปตรงมา)
#
# จุดฝึก (TODO):
# - บังคับเติม citation อัตโนมัติ ถ้าโมเดลลืมใส่ (เช่น ดึงหมายเลขหน้า 1–2 หน้าแรกมาเติม)
# - เพิ่มเครื่องมือ "calculate:" แบบ Router ง่าย ๆ (ดูตัวอย่างด้านล่าง)
# =========================================

import argparse, re
from ollama import Client
from retriever import Retriever

# นโยบายระบบ (ย้ำซ้ำในทุกคำถาม)
SYSTEM_POLICY = """You are a RAG assistant for the World Economic Outlook (WEO).
RULES:
1) Answer ONLY using the provided CONTEXT. If not enough, reply exactly: "I don't have information in WEO for that."
2) Always cite pages as [p.<page>]. Never invent citations.
3) Keep it concise and factual.
"""

def calculator(expr: str) -> str:
    """เครื่องคิดเลขแบบปลอดภัย (ใช้เฉพาะตัวเลขและ + - * / ( ))"""
    if not re.fullmatch(r"[0-9\.\+\-\*\/\(\)\s]+", expr):
        return "Refuse: unsupported expression."
    try:
        return str(eval(expr, {"__builtins__": {}}, {}))
    except Exception as e:
        return f"Error: {e}"

def build_context_snippets(hits):
    """แปลงรายการผลลัพธ์ค้นคืนให้เป็นข้อความ CONTEXT อ่านง่าย
    - รูปแบบ: [C1] (p.12) ข้อความ...
    - LLM จะได้รู้ว่าเนื้อหามาจากหน้าไหน ใช้อ้างอิง [p.หน้า] ได้
    """
    lines = []
    for i, h in enumerate(hits, 1):
        lines.append(f"[C{i}] (p.{h['page']}) {h['text']}")
    return "\n\n".join(lines)

def answer(query: str) -> str:
    """ฟังก์ชันหลักสำหรับตอบคำถามแบบ RAG"""
    # Router ง่าย ๆ: รองรับเครื่องคิดเลขด้วย prefix "calculate:"
    if query.lower().startswith("calculate:"):
        expr = query.split(":", 1)[1].strip()
        return calculator(expr)

    # 1) ดึงชิ้นความรู้จาก Qdrant
    r = Retriever()
    hits = r.query(query, top_k=5)
    if not hits:
        return "I don't have information in WEO for that."

    # 2) สร้าง CONTEXT ให้ LLM
    context = build_context_snippets(hits)

    # 3) ประกอบพรอมต์ชัด ๆ (ย้ำ policy + แนบบริบท + คำถาม)
    prompt = f"""{SYSTEM_POLICY}

CONTEXT:
{context}

USER QUESTION:
{query}

Answer in English with citations like [p.X].
"""

    # 4) เรียก LLM (gemma3:1b) ผ่าน Ollama
    client = Client()
    res = client.chat(model="gemma3:1b", messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt}
    ])
    ans = res["message"]["content"].strip()

    # TODO: ถ้าโมเดลลืมใส่ [p.X] ให้เพิ่มช่วงท้ายโดยใช้หน้า top-1/2 จาก hits
    # hint:
    # pages = sorted({h["page"] for h in hits if h.get("page")})
    # if "[p." not in ans and pages:
    #     ans = ans + " " + " ".join([f"[p.{p}]" for p in pages[:2]])

    return ans

if __name__ == "__main__":
    # โหมดสั่งจาก command line เพื่อทดสอบเร็ว ๆ
    ap = argparse.ArgumentParser(description="ถามตอบกับเอเจนต์ RAG (gemma3:1b + Qdrant)")
    ap.add_argument("--q", required=True, help="คำถาม เช่น --q \"What is the global growth forecast?\"")
    args = ap.parse_args()
    print(answer(args.q))
