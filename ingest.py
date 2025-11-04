import os
import pypdf
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OllamaEmbeddings
from langchain_qdrant import Qdrant

# --- ค่าคงที่ (Constants) ---
PDF_PATH = "data/WEO_April_2024.pdf" # ตำแหน่งไฟล์ PDF ที่จะใช้
COLLECTION_NAME = "weo_april_2024" # ชื่อ Collection (เหมือนตาราง) ใน Qdrant

# --- โหลด Environment Variables ---
load_dotenv() # โหลดค่าจากไฟล์ .env
QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "gemma3:1b") # โหลดชื่อโมเดล, ถ้าไม่ตั้งไว้ให้ใช้ "gemma3:1b"
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434") # URL ของ Ollama

def main():
    """
    ฟังก์ชันหลักสำหรับกระบวนการ Ingestion:
    โหลด PDF -> แบ่งเป็นส่วนย่อย (Chunks) -> แปลงเป็น Vector (Embed) -> อัปโหลดขึ้น Qdrant
    (อ้างอิงเนื้อหา Class 2)
    """
    print("เริ่มต้นกระบวนการ Ingestion...")
    
    # 1. โหลด PDF (Class 2)
    print(f"กำลังโหลด PDF จาก {PDF_PATH}...")
    loader = PyPDFLoader(PDF_PATH)
    
    # 2. แบ่งเอกสาร (Split the Document) (Class 2)
    # TODO: (Class 2, Slide 10) ให้นักเรียนสร้างตัวแปร text_splitter
    # โดยใช้ RecursiveCharacterTextSplitter
    # text_splitter = RecursiveCharacterTextSplitter(
    #     chunk_size=1000,  # ขนาดแต่ละ chunk (ตัวอักษร)
    #     chunk_overlap=100 # ขนาดส่วนที่ทับซ้อนกัน
    # )
    
    # TODO: (Class 2) โหลดและแบ่งเอกสาร (uncomment บรรทัดล่าง)
    # docs = loader.load_and_split(text_splitter)

    # --- (Optional) ส่วนสำหรับ Debugging ---
    # หลังจาก uncomment ข้างบนแล้ว, ลอง uncomment 3 บรรทัดนี้เพื่อดูผลลัพธ์
    # print(f"แบ่งเอกสารเรียบร้อย. ได้ทั้งหมด {len(docs)} chunks.")
    # print(f"\n--- ตัวอย่าง Chunk ที่ 1 (จากหน้า {docs[0].metadata.get('page')}) ---")
    # print(docs[0].page_content[:500] + "...")
    # print("--------------------------------------------------")
    # -------------------------------------

    # 3. สร้าง Embedding Model (Class 2)
    print(f"กำลังเตรียม Embedding model: {OLLAMA_MODEL}...")
    # TODO: (Class 2) ให้นักเรียนสร้าง OllamaEmbeddings
    # embeddings = OllamaEmbeddings(
    #     model=OLLAMA_MODEL,
    #     base_url=OLLAMA_BASE_URL
    # )

    # 4. อัปโหลดไปยัง Qdrant (Class 2, Slide 21)
    print(f"กำลังเชื่อมต่อ Qdrant ที่ {QDRANT_URL}...")
    
    # TODO: (Class 2) ให้นักเรียนใช้ Qdrant.from_documents เพื่ออัปโหลด
    # คำสั่งนี้จะ:
    # 1. เชื่อมต่อ Qdrant
    # 2. (สำคัญ!) ลบ collection เก่าและสร้างใหม่ (force_recreate=True)
    # 3. ทำการ embed และ อัปโหลดเอกสารทั้งหมด
    #
    # (ข้อควรระวัง: Qdrant.from_documents เหมาะสำหรับ dev เท่านั้น
    # ใน production เราจะใช้ client.add_documents() เพื่ออัปเดต)
    #
    # qdrant = Qdrant.from_documents(
    #     docs,
    #     embeddings,
    #     url=QDRANT_URL,
    #     api_key=QDRANT_API_KEY,
    #     collection_name=COLLECTION_NAME,
    #     force_recreate=True, 
    # )
    
    print(f"--- Ingestion เสร็จสิ้น! ---")
    # TODO: อัปเดตเลข 0 ให้เป็น len(docs) หลังจากทำ TODO ข้างบนเสร็จ
    print(f"อัปโหลด {0} เอกสาร ไปยัง collection '{COLLECTION_NAME}' เรียบร้อย")

if __name__ == "__main__":
    # ตรวจสอบว่า .env มีค่าที่จำเป็นหรือไม่
    if not QDRANT_URL or not QDRANT_API_KEY:
        print("Error: QDRANT_URL หรือ QDRANT_API_KEY ไม่ได้ถูกตั้งค่าใน .env")
    else:
        main()

