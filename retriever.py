import os
from dotenv import load_dotenv
from langchain_community.embeddings import OllamaEmbeddings
from langchain_qdrant import Qdrant
from qdrant_client import QdrantClient

# --- ค่าคงที่ (Constants) ---
COLLECTION_NAME = "weo_april_2024" # ต้องเป็นชื่อเดียวกับใน ingest.py

# --- โหลด Environment Variables ---
load_dotenv()
QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "gemma3:1b")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

def get_retriever(k=5):
    """
    ฟังก์ชันสำหรับสร้าง Retriever (ตัวค้นหา) จาก Qdrant
    (อ้างอิง Class 2, Slide 23 และ Class 3, Slide 14)
    
    Returns:
        Langchain-compatible retriever object
    """
    
    # 1. สร้าง Embedding Model (ต้องเป็นโมเดลเดียวกับตอน ingest)
    embeddings = OllamaEmbeddings(
        model=OLLAMA_MODEL,
        base_url=OLLAMA_BASE_URL
    )
    
    # 2. สร้าง Qdrant client เพื่อเชื่อมต่อ
    # (เราใช้ client ที่เป็นทางการของ Qdrant)
    client = QdrantClient(
        url=QDRANT_URL,
        api_key=QDRANT_API_KEY,
    )
    
    # 3. สร้าง LangChain Qdrant wrapper
    # (ตัวนี้จะใช้ client ข้างบนในการเชื่อมต่อ)
    qdrant_store = Qdrant(
        client=client,
        collection_name=COLLECTION_NAME,
        embeddings=embeddings,
    )
    
    # 4. แปลง Vector Store ให้เป็น Retriever
    # TODO: (Class 2/3) ให้นักเรียนสร้าง retriever
    # โดยใช้ .as_retriever() และตั้งค่า 'k' (จำนวน chunk ที่จะดึง)
    # retriever = qdrant_store.as_retriever(
    #     search_type="similarity", # ค้นหาแบบ similarity
    #     search_kwargs={'k': k}    # ดึง k ผลลัพธ์
    # )
    
    # TODO: แก้ return None เป็น return retriever
    return None 

# --- ส่วนสำหรับทดสอบ (Test Block) ---
if __name__ == "__main__":
    """
    รันไฟล์นี้โดยตรง (python retriever.py) เพื่อทดสอบว่า Retriever ทำงานถูกต้องหรือไม่
    """
    print("กำลังทดสอบ Retriever...")
    
    # TODO: ให้นักเรียน uncomment 5 บรรทัดล่างนี้หลังจากทำ get_retriever เสร็จ
    # test_retriever = get_retriever(k=3)
    # query = "What is the GDP growth for Thailand?"
    # results = test_retriever.invoke(query)
    
    # print(f"\n--- ผลการค้นหาสำหรับ: '{query}' ---")
    # for i, doc in enumerate(results):
    #     print(f"\n--- ผลลัพธ์ที่ {i+1} (Page {doc.metadata.get('page')}) ---")
    #     print(doc.page_content[:500] + "...")
    # print("---------------------------------")
    pass

