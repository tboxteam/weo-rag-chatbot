import os
import re # (สำหรับ Calculator)
from dotenv import load_dotenv
from langchain_ollama.chat_models import ChatOllama
from langchain_core.tools import tool
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.messages import HumanMessage, AIMessage

# Import retriever ของเราจากไฟล์ retriever.py
from retriever import get_retriever

# --- โหลด Environment Variables ---
load_dotenv()
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "gemma3:1b")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

# === 1. สร้าง Tools (Class 3, Slide 14-15) ===

# --- Tool 1: WEO Retriever Tool ---
# TODO: (Class 3) ให้นักเรียนสร้าง weo_retriever
# โดยเรียกใช้ get_retriever()
# weo_retriever = get_retriever(k=5) # ดึงมา 5 chunks

@tool
def weo_retriever_tool(query: str) -> str:
    """
    (นี่คือ Docstring ที่สำคัญมาก! Agent จะอ่านสิ่งนี้เพื่อตัดสินใจ)
    ใช้เครื่องมือนี้ 'เฉพาะ' เมื่อตอบคำถามเกี่ยวกับ World Economic Outlook (WEO),
    เศรษฐกิจ (economy), GDP, เงินเฟ้อ (inflation), หรือหัวข้อที่เกี่ยวข้อง
    Input ของเครื่องมือนี้ต้องเป็นคำถามที่เฉพาะเจาะจง (specific query)
    """
    # TODO: (Class 3) ให้นักเรียน uncomment ส่วนนี้
    # print(f"--- [Agent] กำลังเรียก WEO Retriever Tool ด้วย query: {query} ---")
    
    # TODO: (Class 3) เรียก retriever และ format ผลลัพธ์
    # (อ้างอิง Class 3, Slide 14)
    # docs = weo_retriever.invoke(query)
    # context = ""
    # for doc in docs:
    #     context += f"[Source: {doc.metadata.get('source', 'N/A')}, Page: {doc.metadata.get('page', 'N/A')}]\n"
    #     context += doc.page_content + "\n---\n"
    
    # return context
    return "TODO: Implement weo_retriever_tool" # (ลบ/แก้ไข บรรทัดนี้)

@tool
def calculator_tool(expression: str) -> str:
    """
    (Docstring สำคัญ!)
    ใช้เครื่องมือนี้ 'เฉพาะ' เมื่อต้องการคำนวณทางคณิตศาสตร์
    Input ต้องเป็นนิพจน์คณิตศาสตร์ที่ถูกต้อง (เช่น '2+2', '5*4.5')
    """
    # TODO: (Class 3) ให้นักเรียน uncomment ส่วนนี้
    # print(f"--- [Agent] กำลังเรียก Calculator Tool ด้วย expression: {expression} ---")
    
    # (ข้อควรระวัง: eval() ไม่ปลอดภัยใน Production จริง)
    # (สำหรับ Workshop นี้ เราใช้เพื่อความง่าย)
    # try:
    #     # ตรวจสอบว่ามีเฉพาะตัวเลขและเครื่องหมายที่อนุญาต
    #     if not re.match(r"^[0-9\.\+\-\*\/\(\) ]+$", expression):
    #         return "Error: Invalid characters in expression"
    #     result = eval(expression)
    #     return str(result)
    # except Exception as e:
    #     return f"Error calculating: {str(e)}"
    
    return "TODO: Implement calculator_tool" # (ลบ/แก้ไข บรรทัดนี้)


# === 2. สร้าง Agent Policy (Prompt) (Class 3, Slide 16) ===

# TODO: (Class 3) ให้นักเรียนเขียน System Prompt (Agent Policy)
# (ดูตัวอย่างจาก Class 3, Slide 16)
SYSTEM_PROMPT = """
You are a helpful AI assistant...
... (ใส่ Policy ที่นี่) ...
"""

# สร้าง Prompt Template
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", SYSTEM_PROMPT),
        MessagesPlaceholder(variable_name="chat_history"), # ที่สำหรับเก็บประวัติแชท
        ("human", "{input}"), # คำถามจาก User
        MessagesPlaceholder(variable_name="agent_scratchpad"), # "กระดาษทด" ของ Agent
    ]
)

# === 3. สร้าง Agent Executor (Class 3, Slide 17) ===

def get_agent_executor():
    """
    ฟังก์ชันสำหรับสร้าง Agent Executor (ตัวรัน Agent)
    """
    print("กำลังสร้าง Agent Executor...")
    
    # 1. รวม Tools ทั้งหมด
    tools = [weo_retriever_tool, calculator_tool]
    
    # 2. เลือก LLM (Brain)
    llm = ChatOllama(
        model=OLLAMA_MODEL,
        base_url=OLLAMA_BASE_URL
    )
    
    # 3. สร้าง Agent (LLM + Prompt + Tools)
    agent = create_tool_calling_agent(llm, tools, prompt)
    
    # 4. สร้าง AgentExecutor (ตัวรัน Loop ของ ReAct)
    # TODO: (Class 3) ให้นักเรียนสร้าง AgentExecutor
    # agent_executor = AgentExecutor(
    #     agent=agent,
    #     tools=tools,
    #     verbose=True # <-- ตั้งเป็น True เพื่อดู ReAct Loop (สำคัญมาก!)
    # )
    
    # TODO: แก้ return None เป็น return agent_executor
    return None

# --- ส่วนสำหรับทดสอบ (Test Block) ---
if __name__ == "__main__":
    """
    รันไฟล์นี้โดยตรง (python agent.py) เพื่อทดสอบว่า Agent ทำงานถูกต้องหรือไม่
    (อ้างอิง Class 3, Slide 18)
    """
    print("กำลังทดสอบ Agent Executor...")
    
    # TODO: ให้นักเรียน uncomment ส่วนนี้หลังจากทำ get_agent_executor() เสร็จ
    
    # agent_executor = get_agent_executor()
    # chat_history = [] # เริ่มต้นประวัติแชท (ว่าง)

    # --- Test 1: WEO Question ---
    # print("\n--- [Test 1] คำถามเกี่ยวกับ WEO ---")
    # q1 = "What is the 2025 GDP growth for Thailand?"
    # response1 = agent_executor.invoke({"input": q1, "chat_history": chat_history})
    # print(f"Answer: {response1['output']}")
    
    # (อัปเดต History)
    # chat_history.extend([
    #     HumanMessage(content=q1),
    #     AIMessage(content=response1["output"])
    # ])

    # --- Test 2: Math Question ---
    # print("\n--- [Test 2] คำถามคณิตศาสตร์ ---")
    # q2 = "What is 4.5 * 2?"
    # response2 = agent_executor.invoke({"input": q2, "chat_history": chat_history})
    # print(f"Answer: {response2['output']}")
    
    # (อัปเดต History)
    # chat_history.extend([
    #     HumanMessage(content=q2),
    #     AIMessage(content=response2["output"])
    # ])

    # --- Test 3: Off-topic (Refusal) ---
    # print("\n--- [Test 3] คำถาม Off-topic (ที่ Agent ควรปฏิเสธ) ---")
    # q3 = "What is the weather in Bangkok?"
    # response3 = agent_executor.invoke({"input": q3, "chat_history": chat_history})
    # print(f"Answer: {response3['output']}")
    pass

