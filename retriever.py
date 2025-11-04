# REPO: weo-rag-chatbot
# FILE: retriever.py
# ==============================
# บทบาทไฟล์นี้ (Retrieval)
# - รับคำถาม (query) จากผู้ใช้
# - แปลง query เป็นเวกเตอร์ด้วยโมเดลเดียวกับตอน ingest (ต้อง "ตรงกัน")
# - เรียก Qdrant ให้คืน Top-K ชิ้นความรู้ที่ "ใกล้ความหมาย" สูงสุด
# - (ทางเลือก) กรองด้วย SCORE_THRESHOLD เพื่อตัด noise ออก
#
# แนวคิด:
# - "ใกล้" ในที่นี้หมายถึง "ใกล้เชิงความหมาย" วัดด้วย cosine similarity ของเวกเตอร์
# - normalize_embeddings=True ทั้งตอน ingest/query เพื่อใช้ COSINE ได้ถูกต้อง
# - TOP_K: ยิ่งมาก LLM ยิ่งมีบริบทเยอะ แต่ยาว/ช้าเกินไปก็ไม่ดี ต้องลองปรับ
# ==============================

import os, argparse
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient

# โหลดคอนฟิกจาก .env
load_dotenv()
QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
QDRANT_COLLECTION = os.getenv("QDRANT_COLLECTION", "WEO_RAG")
EMB_MODEL_NAME = os.getenv("EMB_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
TOP_K = int(os.getenv("TOP_K", "5"))
SCORE_THRESHOLD = float(os.getenv("SCORE_THRESHOLD", "0.20"))

class Retriever:
    def __init__(self):
        # สร้างคลาสเชื่อม Qdrant และเตรียมโมเดลฝั่ง embedding
        self.client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)
        self.model = SentenceTransformer(EMB_MODEL_NAME)

    def query(self, q: str, top_k: int = TOP_K):
        # แปลงคำถามเป็นเวกเตอร์ (normalize ให้พร้อมใช้ COSINE)
        qvec = self.model.encode([q], normalize_embeddings=True)[0]

        # เรียกค้นหาใน Qdrant: คืนเอกสารที่ "คล้าย" มากที่สุดตามเวกเตอร์
        res = self.client.search(
            collection_name=QDRANT_COLLECTION,
            query_vector=qvec.tolist(),
            limit=top_k,
            with_payload=True,  # ขอ payload (page/text) กลับมาด้วย
        )

        # แปลงผลลัพธ์ให้อ่านง่าย
        hits = []
        for p in res:
            score = float(p.score)  # สำหรับ COSINE: "ยิ่งมากยิ่งใกล้"
            # TODO: เปิดใช้ threshold เพื่อตัดผลที่ไม่เกี่ยวข้องมากพอ
            # if score < SCORE_THRESHOLD:
            #     continue
            hits.append({
                "score": score,
                "page": p.payload.get("page"),
                "text": p.payload.get("text", "")
            })
        return hits

if __name__ == "__main__":
    # โหมดสั่งจาก command line เพื่อทดลองเร็ว ๆ
    ap = argparse.ArgumentParser(description="ทดลองค้นจาก Qdrant ด้วยเวกเตอร์")
    ap.add_argument("--q", required=True, help="ข้อความคำถาม/สิ่งที่อยากค้นหา")
    args = ap.parse_args()

    r = Retriever()
    out = r.query(args.q)

    # แสดงผลแบบย่อ: คะแนน + เลขหน้า + ตัวอย่างข้อความ
    for i, h in enumerate(out, 1):
        preview = h["text"].replace("\n", " ")[:120]
        print(f"[{i}] score={h['score']:.3f} page={h['page']}  {preview}...")
