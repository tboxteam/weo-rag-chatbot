# REPO: weo-rag-chatbot
# FILE: README.md
WEO RAG Chatbot — Student Starter (โครงพร้อมคอมเมนต์สอนจากศูนย์)

ภาพรวม (อ่านครั้งเดียวก่อนลงมือ)
- โปรเจกต์นี้สาธิต RAG (Retrieval-Augmented Generation) แบบง่าย:
  1) แยกข้อความจาก PDF (weo.pdf) → ทำ "เวกเตอร์" ด้วยโมเดลฝั่ง embeddings (Sentence-Transformers)
  2) เก็บเวกเตอร์ไว้ใน Qdrant (Vector DB) เพื่อให้ค้นหา Top-K ได้เร็ว
  3) เวลาใช้งาน: ค้นชิ้นความรู้ที่ใกล้คำถามที่สุด (Top-K) → ส่งเข้า LLM (gemma3:1b บน Ollama) ให้สรุปพร้อมอ้างอิงหน้า
- ทุกไฟล์อยู่ root โฟลเดอร์ เพื่อให้นักเรียนที่เพิ่งเริ่มสามารถรันได้ง่าย

เริ่มต้นใช้งาน (สรุป)
1) ติดตั้ง Python 3.10+  
2) ติดตั้งไลบรารี: `pip install -r requirements.txt`  
3) ติดตั้ง/เปิด Ollama และดึงโมเดล: `ollama pull gemma3:1b` แล้ว `ollama serve`  
4) คัดลอก `.env.example` เป็น `.env` แล้วเติมค่าจริงของ Qdrant Cloud (URL, API Key)  
5) วางไฟล์จริง `data/weo.pdf` (ผู้สอนจะให้ไฟล์นี้)  
6) สร้างดัชนี: `python ingest.py`  
7) ทดลองค้นคืน: `python retriever.py --q "What is Thailand's 2025 GDP growth?"`  
8) ถามผ่านเอเจนต์ RAG: `python agent.py --q "Summarize key risks for Asian economy."`  
9) UI ตัวอย่าง: `streamlit run app.py`

หมายเหตุสำหรับผู้เรียน (เช็กพอยต์ที่ควรลองแก้)
- TODO ในแต่ละไฟล์คือการบ้าน/จุดฝึก: ปรับ chunk size, ปรับ threshold, บังคับ citation, ฯลฯ
- แนวคิดหลัก:
  • Embedding = การแปลงข้อความเป็นตัวเลขหลายมิติ (เวกเตอร์) ให้คอมพิวเตอร์วัด "ความใกล้ความหมาย" ได้  
  • Vector DB (Qdrant) = ฐานข้อมูลที่ออกแบบมาเพื่อค้นหาเวกเตอร์ Top-K เร็ว ๆ (เช่นใช้ HNSW)  
  • Cosine Similarity = ค่าความใกล้เชิงมุม (ยิ่งมากยิ่งใกล้) ใช้คู่กับการ normalize เวกเตอร์  
  • RAG = ดึงชิ้นความรู้จริงมากำกับ LLM เพื่อ "อ้างอิงได้" และลดการเดา

Advanced (เลือกทำ): ใช้ Qdrant แบบ Local (Docker) แล้วแก้ `QDRANT_URL=http://localhost:6333`
