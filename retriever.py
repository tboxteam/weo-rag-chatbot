import os
from dotenv import load_dotenv
from qdrant_client import QdrantClient
# (แก้ไข 1) Import ให้ถูกต้องตาม ingest.py
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_qdrant import QdrantVectorStore

# --- ค่าคงที่ (Constants) ---
# (เราใช้ค่าเดียวกับ ingest.py)
COLLECTION_NAME = "weo_april_2024"
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2" 

# --- โหลด Environment Variables ---
load_dotenv() # โหลดค่าจากไฟล์ .env
QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")

# --- ค่าคงที่สำหรับ Retriever ---
# (Class 2, Slide 12) เราจะดึง Top-K chunks ที่เกี่ยวข้อง
# K = 3 หมายถึง ดึงมา 3 chunks ที่คะแนนดีที่สุด
RETRIEVER_K = 3

def get_retriever():
    """
    ฟังก์ชันนี้ทำหน้าที่สร้างและ return "Retriever"
    Retriever คือ object ที่ LangChain ใช้ในการ "ค้นหา" (Search)
    ข้อมูลที่เกี่ยวข้องจาก Vector Database (Qdrant)
    
    (อ้างอิง Class 2, Slide 12, 16, 21)
    """
    
    # 1. สร้าง Embedding Model (ต้องใช้ "ตัวเดียว" กับตอน ingest)
    print(f"กำลังโหลด Embedding model: {EMBEDDING_MODEL_NAME}...")
    # TODO: (Class 2) ให้นักเรียนสร้าง Embedding model
    # (ต้องเป็น model เดียวกับ ingest.py)
    # embeddings = HuggingFaceEmbeddings(
    #     model_name=EMBEDDING_MODEL_NAME,
    #     model_kwargs={'device': 'cpu'}
    # )

    # 2. สร้าง Qdrant Client (ตัวเชื่อมต่อ Qdrant)
    # TODO: (Class 2) ให้นักเรียนสร้าง Qdrant Client
    # client = QdrantClient(
    #     url=QDRANT_URL,
    #     api_key=QDRANT_API_KEY,
    # )

    # 3. สร้าง Qdrant Vector Store (ตัวจัดการ Collection)
    # (แก้ไข 2) ใช้ QdrantVectorStore (ตัวใหม่)
    # TODO: (Class 2) ให้นักเรียนสร้าง Qdrant Vector Store
    # qdrant_store = QdrantVectorStore(
    #     client=client,
    #     collection_name=COLLECTION_NAME,
    #     embedding=embeddings, 
    # )

    # 4. สร้าง Retriever
    # .as_retriever() คือการแปลง Vector Store ให้เป็น "Retriever"
    # ที่ LangChain (Agent) สามารถเรียกใช้ได้
    # search_kwargs={"k": RETRIEVER_K} คือการบอกว่า "ฉันต้องการ Top-K"
    
    # TODO: (Class 2/3) ให้นักเรียนสร้าง retriever จาก qdrant_store
    # retriever = qdrant_store.as_retriever(
    #     search_kwargs={"k": RETRIEVER_K}
    # )
    
    # (uncomment 2 บรรทัดล่างนี้ หลังจากทำ TODO ข้างบนเสร็จ)
    # print("Retriever พร้อมใช้งาน")
    # return retriever 
    
    # (สำหรับ Starter: คืนค่า None ก่อน)
    return None

# --- ส่วนสำหรับทดสอบ Retriever (รันไฟล์นี้โดยตรง) ---
if __name__ == "__main__":
    """
    นี่คือส่วนที่จะรันเมื่อเราสั่ง `python retriever.py`
    เพื่อทดสอบว่า Retriever ทำงานถูกต้องหรือไม่
    """
    
    # ตรวจสอบ .env
    if not QDRANT_URL or not QDRANT_API_KEY:
        print("Error: QDRANT_URL หรือ QDRANT_API_KEY ไม่ได้ถูกตั้งค่าใน .env")
    else:
        print("กำลังทดสอบ Retriever...")
        
        # TODO: (Class 2) ให้นักเรียน uncomment 2 บรรทัดล่าง
        # หลังจากทำฟังก์ชัน get_retriever() เสร็จแล้ว
        
        test_retriever = get_retriever()
        
        # (เมื่อ uncomment แล้ว Error 'NoneType' object... จะหายไป)
        if test_retriever:
            query = "What is the GDP growth forecast for Thailand in 2025?"
            print(f"กำลังค้นหาด้วยคำถาม: {query}\n")
            
            # .invoke() คือการสั่งให้ Retriever ทำงาน
            results = test_retriever.invoke(query)
            
            print("\n--- ผลลัพธ์ (Contexts) ที่เกี่ยวข้อง ---")
            for i, doc in enumerate(results):
                print(f"\n--- Chunk {i+1} (Source: {doc.metadata.get('source')}, Page: {doc.metadata.get('page')}) ---")
                print(doc.page_content)
        else:
            print("Retriever ยังไม่ถูกสร้าง (กรุณาทำ TODO ใน get_retriever)")

        # (สำหรับ Starter: แสดง TODO)
        print("กรุณาเข้าไปแก้ไขโค้ด `retriever.py` และ uncomment ส่วน `TODO`")