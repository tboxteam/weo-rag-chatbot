# REPO: weo-rag-chatbot
# FILE: eval.py
# =========================================
# บทบาทไฟล์นี้ (การประเมินเบื้องต้น)
# - รันคำถามจากไฟล์ .jsonl ทีละบรรทัด
# - วัดเวลา (latency) และเช็กว่าคำตอบมี citation [p.X] หรือไม่
# - จุดประสงค์: ให้ผู้เรียนเห็น "ผลกระทบ" ของการปรับ TOP_K, threshold, chunk size
#
# จุดฝึก (TODO):
# - เพิ่มตัวชี้วัดความถูกต้อง (เช่นนับจำนวน [p.X] ที่ตรงหน้า "จริง")
# - บันทึกผลเป็น CSV/JSON เพื่อง่ายต่อการสรุปในคลาส
# - วัดสถิติ latency (mean, p95) สำหรับกลุ่มคำถามใหญ่ขึ้น
# =========================================

import argparse, json, time, re
from agent import answer

def has_citation(ans: str) -> bool:
    """ตรวจว่ามีรูปแบบอ้างอิง [p.ตัวเลข] ในคำตอบหรือไม่ (เช็กหยาบ ๆ)"""
    return bool(re.search(r"\[p\.\d+\]", ans))

def main():
    ap = argparse.ArgumentParser(description="ประเมินผลลัพธ์ของ RAG แบบง่าย")
    ap.add_argument("--file", required=True, help="ไฟล์ .jsonl ที่มีรายการคำถามทดสอบ")
    args = ap.parse_args()

    # โหลดคำถามทั้งหมดจากไฟล์ .jsonl (บรรทัดละ 1 JSON object)
    with open(args.file, "r", encoding="utf-8") as f:
        items = [json.loads(x) for x in f if x.strip()]

    # รันทีละคำถามและเก็บผล
    results = []
    for item in items:
        t0 = time.time()
        ans = answer(item["q"])
        dt = time.time() - t0
        results.append({
            "id": item["id"],
            "q": item["q"],
            "latency_sec": round(dt, 2),
            "has_citation": has_citation(ans),
            "answer": ans
        })

    # แสดงผลลัพธ์บนคอนโซล (อ่านง่าย)
    for r in results:
        print(f"#{r['id']} latency={r['latency_sec']}s  citation={r['has_citation']}")
        print(r["answer"].strip(), "\n")

if __name__ == "__main__":
    main()
