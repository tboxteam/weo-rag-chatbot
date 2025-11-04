# REPO: weo-rag-chatbot (student)
# FILE: ingest.py
# ============================================================
# Ingestion Pipeline (ฉบับแก้ไขให้ "ตัดตามโทเคน" แทนตัวอักษร)
#
# ทำไมต้องตัดตามโทเคน:
# - โมเดล embedding (all-MiniLM-L6-v2) รับความยาวประมาณ ~256 โทเคน
# - ถ้า chunk ยาวเกิน โมเดลจะ "ตัดท้าย" (truncate) → เนื้อหาท้ายชิ้นหาย → recall แย่ลง
# - ทางแก้: จำกัดความยาวชิ้นด้วย "จำนวนโทเคน" + ทำ overlap เล็กน้อย
#
# โครงสร้าง:
# 1) อ่าน PDF รายหน้า → ได้ข้อความทั้งหน้า
# 2) แปลงทั้งหน้าเป็นโทเคน (ด้วย tokenizer ของโมเดล embedding เดียวกัน)
# 3) สไลด์วินโดว์ทีละ CHUNK_TOKENS โทเคน พร้อมทับซ้อน CHUNK_OVERLAP_TOKENS
# 4) ถอดโทเคนกลับเป็นข้อความ แล้วไปทำ embedding + upsert ขึ้น Qdrant
#
# จุดที่ผู้เรียนลองปรับ (TODO):
# - CHUNK_TOKENS: 160–220 (แนะนำเริ่ม 200)  ใหญ่ไป = เสี่ยงโดน truncate; เล็กไป = ได้ชิ้นเยอะ/บริบทแตก
# - CHUNK_OVERLAP_TOKENS: 20–60 (แนะนำเริ่ม 40) กันคำสำคัญตกหล่นตรงรอยต่อ
# - เปลี่ยน "ตัดตามหน้า" เป็น "ตัดตามหัวข้อ/ย่อหน้า" ก่อน แล้วค่อยทำสไลด์โทเคน (ขั้นสูง)
# ============================================================

import os, uuid
from typing import List, Dict
from dotenv import load_dotenv
from pypdf import PdfReader
from tqdm import tqdm
import numpy as np

from sentence_transformers import SentenceTransformer
from transformers import AutoTokenizer  # ใช้ tokenizer ของโมเดล embedding เดียวกัน

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct

# โหลดคอนฟิกจาก .env
load_dotenv()
QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
QDRANT_COLLECTION = os.getenv("QDRANT_COLLECTION", "WEO_RAG")
EMB_MODEL_NAME = os.getenv("EMB_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
EMB_DIM = int(os.getenv("EMB_DIM", "384"))

# ตำแหน่งไฟล์ PDF (ผู้สอนจะวางไฟล์จริง)
DATA_PDF = os.path.join("data", "weo.pdf")

# พารามิเตอร์ตัดชิ้นตาม "โทเคน"
CHUNK_TOKENS = 200           # TODO: ปรับ 160–220 ตามคุณภาพผลลัพธ์
CHUNK_OVERLAP_TOKENS = 40    # TODO: ปรับ 20–60 เพื่อกันคำหล่นตรงรอยต่อ

def read_pdf_text(path: str) -> List[str]:
    """อ่าน PDF รายหน้า → คืน list[str] ข้อความของแต่ละหน้า
    - ถ้าเป็นสแกน (รูปภาพ) จะได้สตริงว่าง ต้องทำ OCR เพิ่ม (นอกขอบเขตแลบนี้)
    """
    assert os.path.exists(path), f"Missing PDF: {path}"
    reader = PdfReader(path)
    return [(page.extract_text() or "") for page in reader.pages]

def chunk_page_by_tokens(page_text: str, tokenizer) -> List[str]:
    """ตัด 'ข้อความ 1 หน้า' เป็นหลายชิ้น ตามจำนวนโทเคน
    - สไลด์วินโดว์: ขนาด CHUNK_TOKENS, เลื่อนไปครั้งละ (CHUNK_TOKENS - CHUNK_OVERLAP_TOKENS)
    - ข้อดี: ไม่โดน truncate เพราะเราไม่เกินลิมิตที่ตั้งเอง
    - หมายเหตุ: ตัดแบบไม่ยึดประโยค อาจได้ชิ้นที่ตัดกลางประโยค (พอรับได้สำหรับแลบเริ่มต้น)
      ผู้เรียนที่อยากสวยงามขึ้น ลองตัดตามประโยค/ย่อหน้า แล้วแตกย่อยเป็นโทเคนอีกที (ขั้นสูง)
    """
    if not page_text.strip():
        return []

    # แปลงข้อความทั้งหน้า → โทเคนไอดี (ไม่ใส่ special tokens)
    ids = tokenizer.encode(page_text, add_special_tokens=False)
    if not ids:
        return []

    chunks: List[str] = []
    step = max(1, CHUNK_TOKENS - CHUNK_OVERLAP_TOKENS)  # กันศูนย์/ติดลูป
    start = 0
    n = len(ids)

    while start < n:
        end = min(start + CHUNK_TOKENS, n)
        piece_ids = ids[start:end]
        # ถอดกลับเป็นข้อความธรรมชาติ (skip_special_tokens=True เพื่อไม่ให้โผล่โทเคนพิเศษ)
        text_chunk = tokenizer.decode(piece_ids, skip_special_tokens=True).strip()
        if text_chunk:
            chunks.append(text_chunk)
        if end == n:
            break
        start += step

    return chunks

def build_payloads(pages_text: List[str], tokenizer) -> List[Dict]:
    """วนทุกหน้า → ตัดเป็นหลายชิ้นตามโทเคน → ติดป้ายกำกับ page เพื่อไว้ทำ citation"""
    payloads: List[Dict] = []
    for page_idx, page_text in enumerate(pages_text, start=1):
        tiny_chunks = chunk_page_by_tokens(page_text, tokenizer)
        for t in tiny_chunks:
            payloads.append({"page": page_idx, "text": t})
    return payloads

def main():
    # 0) ตรวจไฟล์และคอนฟิกพื้นฐาน
    assert os.path.exists(DATA_PDF), "ไม่พบ data/weo.pdf (ผู้สอนจะวางไฟล์ให้)"
    assert QDRANT_URL, "กรุณาเติม QDRANT_URL ใน .env"
    # API key ของ Qdrant Cloud อาจว่างได้ หากคลัสเตอร์ตั้งค่าอนุญาต (แต่โดยปกติควรมี)

    # 1) เตรียมโมเดล embedding และ tokenizer ให้ "คู่กัน"
    #    สำคัญ: ต้องใช้โมเดลเดียวกันทั้งตอน ingest และตอนค้น (retrieval)
    model = SentenceTransformer(EMB_MODEL_NAME)
    tokenizer = AutoTokenizer.from_pretrained(EMB_MODEL_NAME)

    # 2) ต่อ Qdrant
    client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)

    # 3) สร้าง collection ถ้ายังไม่มี (ขนาดเวกเตอร์ต้องตรงกับโมเดล: 384 สำหรับ all-MiniLM-L6-v2)
    existing = [c.name for c in client.get_collections().collections]
    if QDRANT_COLLECTION not in existing:
        client.create_collection(
            collection_name=QDRANT_COLLECTION,
            vectors_config=VectorParams(size=EMB_DIM, distance=Distance.COSINE)  # ใช้ COSINE เพราะเราจะ normalize
        )

    # 4) อ่าน PDF รายหน้า → แตกเป็นชิ้นตามโทเคน (พร้อม overlap)
    pages_text = read_pdf_text(DATA_PDF)
    payloads = build_payloads(pages_text, tokenizer)   # [{'page': 1, 'text': '...'}, ...]

    # 5) ทำ embedding (normalize=True เพื่อจับคู่ด้วย COSINE)
    texts = [p["text"] for p in payloads]
    vecs = model.encode(texts, batch_size=64, show_progress_bar=True, normalize_embeddings=True)

    # 6) อัปโหลดเข้า Qdrant (เก็บทั้งเวกเตอร์ + payload: page/text)
    points = []
    for payload, vec in tqdm(zip(payloads, vecs), total=len(payloads), desc="Upserting to Qdrant"):
        points.append(PointStruct(
            id=str(uuid.uuid4()),
            vector=np.asarray(vec, dtype=np.float32).tolist(),
            payload=payload
        ))

    client.upsert(collection_name=QDRANT_COLLECTION, points=points)
    print(f"✅ Upserted {len(points)} chunks (token-based) to '{QDRANT_COLLECTION}' on Qdrant Cloud.")
    print(f"Info: CHUNK_TOKENS={CHUNK_TOKENS}, OVERLAP={CHUNK_OVERLAP_TOKENS}, pages={len(pages_text)}")

if __name__ == "__main__":
    main()
