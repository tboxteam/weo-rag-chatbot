import os
import pypdf
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings # (Import ตาม Deprecation Warning)
from langchain_qdrant import QdrantVectorStore # (แก้ไข 1) เปลี่ยนจาก Qdrant
from qdrant_client import QdrantClient 
from qdrant_client.http import models # <<< (เพิ่ม) Import models สำหรับ VectorParams
from tqdm import tqdm 

# --- ค่าคงที่ (Constants) ---
PDF_PATH = "data/WEO_April_2024.pdf" # (สมมติว่าไฟล์อยู่ใน folder data)
COLLECTION_NAME = "weo_april_2024" # ชื่อ Collection (เหมือนตาราง) ใน Qdrant

# ชื่อ Embedding model ที่เราจะใช้
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2" 
EMBEDDING_MODEL_DIMENSION = 384 # <<< (เพิ่ม) จำนวนมิติของโมล (สำหรับ all-MiniLM-L6-v2)
# ขนาด Batch ที่จะส่งให้ Qdrant (แก้ปัญหา Timeout)
BATCH_SIZE = 32 # <<< (แก้ไข 1) ลดขนาด Batch ลงเหลือ 32
# พารามิเตอร์สำหรับ Text Splitter
EMBEDDING_CHUNK_SIZE = 1000 # ขนาดแต่ละ chunk (ตัวอักษร)
EMBEDDING_CHUNK_OVERLAP = 100 # ขนาดส่วนที่ทับซ้อนกัน

# --- โหลด Environment Variables ---
load_dotenv() # โหลดค่าจากไฟล์ .env
QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")

def main():
    """
    ฟังก์ชันหลักสำหรับ Ingestion
    (โหลด, แบ่ง, Embed, และ อัปโหลด PDF ไปยัง Qdrant)
    """
    print("เริ่มต้นกระบวนการ Ingestion...")
    
    # 1. โหลด PDF (Class 2, Slide 10)
    print(f"กำลังโหลด PDF จาก {PDF_PATH}...")
    # TODO: (Class 2) ให้นักเรียนสร้าง loader และ โหลดเอกสาร
    # loader = PyPDFLoader(PDF_PATH)
    
    # 2. แบ่งเอกสาร (Split the Document) (Class 2)
    # TODO: (Class 2, Slide 10) ให้นักเรียนสร้างตัวแปร text_splitter
    # โดยใช้ RecursiveCharacterTextSplitter
    # text_splitter = RecursiveCharacterTextSplitter(
    #     chunk_size=EMBEDDING_CHUNK_SIZE,
    #     chunk_overlap=EMBEDDING_CHUNK_OVERLAP
    # )
    
    # TODO: (Class 2) โหลดและแบ่งเอกสาร (uncomment บรรทัดล่าง)
    # (เราจะใช้ .load_and_split() ทีเดียว)
    # docs = loader.load_and_split(text_splitter)
    
    print(f"แบ่งเอกสารเรียบร้อย. ได้ทั้งหมด {len(docs)} chunks.")

    # (uncomment 4 บรรทัดล่างเพื่อ debug chunk แรก)
    print("\n--- ตัวอย่าง Chunk ที่ 1 (จากหน้า 0) ---")
    print(docs[0].page_content)
    print(f"Metadata: {docs[0].metadata}")
    print("--------------------------------------------------")

    # 3. สร้าง Embedding Model (Class 2)
    print(f"กำลังเตรียม Embedding model: {EMBEDDING_MODEL_NAME}...")
    # TODO: (Class 2) ให้นักเรียนสร้าง Embedding model
    # (โมเดลนี้จะถูกดาวน์โหลดมาเก็บใน cache ครั้งแรกที่รัน)
    # embeddings = HuggingFaceEmbeddings(
    #     model_name=EMBEDDING_MODEL_NAME,
    #     model_kwargs={'device': 'cpu'} # บังคับให้ใช้ CPU (ถ้าเครื่องนักเรียนไม่มี GPU)
    # )

    # 4. อัปโหลดไปยัง Qdrant (Class 2, Slide 21)
    print(f"กำลังเชื่อมต่อ Qdrant ที่ {QDRANT_URL}...")
    
    # TODO: (Class 2) ให้นักเรียน uncomment โค้ดข้างล่าง
    # เพื่อสร้าง Client และ Qdrant vector store
    
    # 1. สร้าง Qdrant Client (จาก qdrant_client)
    # client = QdrantClient(
    #     url=QDRANT_URL,
    #     api_key=QDRANT_API_KEY,
    # )

    # 2. สร้าง Qdrant Vector Store wrapper (จาก langchain_qdrant)
    #    (เราส่ง client ที่สร้างไว้เข้าไป)
    # qdrant = QdrantVectorStore(
    #     client=client,
    #     collection_name=COLLECTION_NAME,
    #     embedding=embeddings, # (แก้จาก embeddings (มี s))
    # )
    
    # (Check-then-Create) เพื่อแก้ DeprecationWarning
    # print(f"ตรวจสอบ Collection '{COLLECTION_NAME}'...")
    # collection_exists = client.collection_exists(collection_name=COLLECTION_NAME)
    
    # if collection_exists:
    #     print("Collection เดิมมีอยู่ จะลบและสร้างใหม่ (Recreating)...")
    #     client.delete_collection(collection_name=COLLECTION_NAME)
    
    # print("กำลังสร้าง Collection ใหม่...")
    # client.create_collection(
    #     collection_name=COLLECTION_NAME,
    #     vectors_config=models.VectorParams( 
    #         size=EMBEDDING_MODEL_DIMENSION,
    #         distance=models.Distance.COSINE
    #     ),
    # )
    # print("สร้าง Collection เรียบร้อย.")
    
    # ใช้ .add_documents() พร้อม BATCH_SIZE (เพื่อแก้ Timeout)
    print(f"กำลังอัปโหลด {len(docs)} chunks (ทีละ {BATCH_SIZE} chunks)...")
    
    # ใช้ tqdm เพื่อแสดง progress bar
    # for i in tqdm(range(0, len(docs), BATCH_SIZE), desc="Uploading to Qdrant"):
    #     batch_docs = docs[i:i + BATCH_SIZE]
    #     qdrant.add_documents(batch_docs)
    
    # print(f"--- Ingestion เสร็จสิ้น! ---")
    # TODO: อัปเดตเลข 0 ให้เป็น len(docs) หลังจากทำ TODO ข้างบนเสร็จ
    print(f"อัปโหลด {0} เอกสาร ไปยัง collection '{COLLECTION_NAME}' เรียบร้อย")

if __name__ == "__main__":
    # เช็คว่า .env ถูกตั้งค่าหรือยัง
    if not QDRANT_URL or not QDRANT_API_KEY:
        print("Error: QDRANT_URL หรือ QDRANT_API_KEY ไม่ได้ถูกตั้งค่าใน .env")
    else:
        main()