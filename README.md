# **WEO-RAG Chatbot Project**

นี่คือโปรเจกต์ Mini-Project (Module 7\) สำหรับสร้าง Chatbot ตอบคำถามจากเอกสาร World Economic Outlook (WEO) โดยใช้สถาปัตยกรรม RAG

## **Project Goal (เป้าหมาย)**

(อ้างอิง Class 1, Slide 2\)

* สร้าง Chatbot ที่ตอบคำถามโดยอ้างอิงข้อมูลจาก WEO PDF  
* ต้องแสดงหลักฐาน (Citations) เช่น หมายเลขหน้า  
* ต้องปฏิเสธ (Refuse) ที่จะตอบคำถามนอกเหนือจากเนื้อหาในเอกสาร

## **How to Run (วิธีรัน)**

**(อ้างอิง Class 1, Slide 23\)**

0. Clone the repository
   git clone https://github.com/tboxteam/weo-rag-chatbot.git

1. Create Virtual Environment:  
   (สร้างและ Activate venv เพื่อแยก environment ของโปรเจกต์)  
   \# (Mac/Linux)  
   python3 \-m venv venv  
   source venv/bin/activate

   \# (Windows)  
   python \-m venv venv  
   .\\venv\\Scripts\\activate

2. **Install Dependencies:**  
   pip install \-r requirements.txt

3. **Set Environment:**  
   * Copy .env.example ไปเป็น .env  
   * กรอก QDRANT\_URL และ QDRANT\_API\_KEY (จาก Qdrant Cloud)  
   * กรอก OLLAMA\_BASE\_URL (ปกติคือ http://localhost:11434) และ OLLAMA\_MODEL (เช่น gemma3:1b)  
   * (Optional) กรอก LANGCHAIN\_API\_KEY (จาก LangSmith)  
4. Run Ollama:  
   (ตรวจสอบให้แน่ใจว่า Ollama service รันอยู่ และได้ดึงโมเดลที่ต้องการแล้ว)  
   \# (ตัวอย่าง: gemma3:1b จาก Class 1, Slide 21\)  
   ollama run gemma3:1b 

5. Ingest Data (Class 2):  
   (ต้องทำครั้งแรก หรือเมื่อ PDF/Chunking strategy เปลี่ยน)  
   python ingest.py

6. **Run the App (Class 4):**  
   streamlit run app.py

## **Agent Policy (กฎของ Agent)**

(อ้างอิง Class 3, Slide 24 / Class 5, Slide 14\)  
นี่คือนโยบายที่เรา "บังคับ" Agent ผ่าน System Prompt

### **1\. Tool Use Policy**

* Agent จะใช้ weo\_retriever\_tool "เฉพาะ" คำถามที่เกี่ยวกับเศรษฐกิจ, GDP, WEO  
* Agent จะใช้ calculator\_tool "เฉพาะ" การคำนวณ

### **2\. Refusal Policy (Guardrail)**

* Agent "ต้อง" ปฏิเสธ (Refuse) คำถาม Off-topic (เช่น อากาศ, กีฬา, "สวัสดี")  
* Agent "ต้อง" ปฏิเสธ ถ้า weo\_retriever\_tool ค้นหาไม่เจอข้อมูล

### **3\. Citation Policy**

* คำตอบ "ทุกครั้ง" ที่มาจาก WEO "ต้อง" อ้างอิงแหล่งที่มา: \[Source: ..., Page: X\]

## **Final Parameters (ค่าที่ใช้)**

(นักเรียนต้องกรอกส่วนนี้หลังจูนระบบเสร็จ)

* **Chunk Size:** ...  
* **Chunk Overlap:** ...  
* **Retriever K:** ...  
* **Reranker:** (Y/N)  
* **LLM Model:** ...  
* **Embedding Model:** ...

## **Metrics Table (Class 5\)**

(อ้างอิง Class 5, Slide 11 & 20\)  
(นักเรียนต้องรัน 10 Qs Bank และกรอกตารางนี้)

| Query (คำถาม) | Answer (คำตอบย่อ) | Latency (sec) | Faithfulness (1/0) | Relevance (1/0) | Ctx Precision (X/k) |
| :---- | :---- | :---- | :---- | :---- | :---- |
| (Q1: Fact-based) |  |  |  |  |  |
| (Q2: Fact-based) |  |  |  |  |  |
| (Q3: Synthesis) |  |  |  |  |  |
| (Q4: Synthesis) |  |  |  |  |  |
| (Q5: Table-based) |  |  |  |  |  |
| (Q6: Table-based) |  |  |  |  |  |
| (Q7: Edge Case) |  |  |  |  |  |
| (Q8: Off-topic) |  |  |  |  |  |
| (Q9: Off-topic) |  |  |  |  |  |
| (Q10: Math) |  |  |  |  |  |

