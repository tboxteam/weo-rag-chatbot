import os
import re # (สำหรับ Calculator)
from dotenv import load_dotenv

# --- Imports ที่ถูกต้องสำหรับ LangChain v1.0.3 ---

# 1. LLM (Ollama)
from langchain_ollama.chat_models import ChatOllama

# 2. Core (ส่วนประกอบหลัก)
from langchain_core.tools import tool
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

# 3. LangGraph Agent - **สำหรับ LangChain v1.0.3**
# from langgraph.prebuilt import create_react_agent
from langchain.agents import create_agent

# 4. Import (Local)
# Import retriever ของเราจากไฟล์ retriever.py
from retriever import get_retriever

# --- โหลด Environment Variables ---
load_dotenv()
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2:3b")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

# === 1. สร้าง Tools (Class 3, Slide 14-15) ===
# TODO: (Class 4) ให้นักเรียน uncomment บรรทัดล่าง
# --- สร้าง weo_retriever ---
# weo_retriever = get_retriever()

# --- Tool 1: WEO Retriever Tool ---
# TODO: (Class 4) ให้นักเรียน uncomment บรรทัดล่าง
@tool
def weo_retriever_tool(query: str) -> str:
    """Use this tool for questions about World Economic Outlook (WEO), economy, GDP, inflation, or related economic topics. Input should be a specific question about economic data."""
    print(f"\n🔍 [WEO Retriever] Query: {query}")
    
    # try:
    #     # เรียก retriever และ format ผลลัพธ์
    #     docs = weo_retriever.invoke(query)
        
    #     if not docs:
    #         return "No relevant information found in the WEO database."
        
    #     context = ""
    #     for doc in docs:
    #         # ดึง 'page'
    #         page_num = doc.metadata.get('page', 'N/A') 
    #         # เพิ่ม 1 (เพราะ PyPDFLoader เริ่มนับหน้า 0)
    #         if isinstance(page_num, int):
    #             page_num += 1
                
    #         source = doc.metadata.get('source', 'N/A')
    #         context += f"[Source: {source}, Page: {page_num}]\n"
    #         context += doc.page_content + "\n---\n"
        
    #     return context
    # except Exception as e:
    #     return f"Error retrieving WEO data: {str(e)}"

# --- Tool 2: Calculator Tool ---
# TODO: (Class 4) ให้นักเรียน uncomment บรรทัดล่าง
@tool
def calculator_tool(expression: str) -> str:
    """Use this tool for mathematical calculations. Input should be a valid mathematical expression like '2+2' or '5*4.5'"""
    print(f"\n🔢 [Calculator] Expression: {expression}")
    
    # try:
    #     # ตรวจสอบว่ามีเฉพาะตัวเลขและเครื่องหมายที่อนุญาต
    #     expression = expression.strip()
    #     if not re.match(r"^[0-9\.\+\-\*\/\(\) ]+$", expression):
    #         return "Error: Invalid characters. Only numbers and +, -, *, /, (), spaces allowed."
        
    #     # คำนวณ
    #     result = eval(expression)
    #     return f"Result: {result}"
    # except ZeroDivisionError:
    #     return "Error: Division by zero"
    # except Exception as e:
    #     return f"Error: {str(e)}"


# === 2. สร้าง System Prompt ===
# TODO: (Class 4) ให้นักเรียน uncomment บรรทัดล่าง
# SYSTEM_PROMPT = """You are an AI assistant for the World Economic Outlook (WEO) report.

# Rules:
# 1. Always call weo_retriever_tool first for economic questions.
# 2. Use ONLY the retrieved context to answer. You may summarize or synthesize within that context.
# 3. If the context is partially relevant, provide the best possible answer based on what is available, but do NOT add numbers or facts not present.
# 4. If the context is completely unrelated, respond:
#    "I do not have information about that in the WEO report."
# 5. For questions outside economics/WEO, reply with the same message.
# 6. For math questions, use calculator_tool."""

# TODO: (Class 4) ลบบรรทัดล่างหลังจากสร้าง SYSTEM_PROMPT แล้ว
SYSTEM_PROMPT = ""

# === 3. สร้าง Agent Executor ===
# TODO: (Class 4) ให้นักเรียน uncomment บรรทัดล่าง
def get_agent_executor():
    """
    สร้าง Agent ด้วย LangGraph (LangChain v1.0.3)
    """
    print("กำลังสร้าง Agent (LangGraph)...")
    
    # # 1. รวม Tools
    # tools = [weo_retriever_tool, calculator_tool]
    
    # # 2. สร้าง LLM
    # llm = ChatOllama(
    #     model=OLLAMA_MODEL,
    #     base_url=OLLAMA_BASE_URL,
    #     temperature=0
    # )
    
    # # 3. สร้าง Agent ด้วย create_agent
    # # ใน v1.0.3 ใช้แค่ model และ tools (ไม่มี state_modifier)
    # agent_executor = create_agent(
    #     model=llm,
    #     tools=tools
    # )
    
    # print("✅ Agent พร้อมใช้งาน!\n")
    # return agent_executor

    # TODO: (Class 4) ลบบรรทัดล่างหลังจากสร้าง agent_executor แล้ว
    return None


# === 4. ฟังก์ชันสำหรับรัน Agent ===
# TODO: (Class 4) ให้นักเรียน uncomment บรรทัดล่าง
def run_agent(agent_executor, query: str, verbose: bool = True):
    """
    รัน Agent
    
    Args:
        agent_executor: Agent จาก create_agent
        query: คำถาม
        verbose: แสดงขั้นตอนหรือไม่
    
    Returns:
        dict: {'input': query, 'output': answer}
    """
    
    # try:
    #     if verbose:
    #         print(f"\n{'='*60}")
    #         print(f"❓ Question: {query}")
    #         print(f"{'='*60}\n")
        
    #     # เตรียม input สำหรับ LangGraph
    #     # ต้องส่งเป็น dict ที่มี "messages" key
    #     inputs = {
    #         "messages": [
    #             SystemMessage(content=SYSTEM_PROMPT),
    #             HumanMessage(content=query)
    #             # HumanMessage(content=f"{SYSTEM_PROMPT}\n\nQuestion: {query}")
    #         ]
    #     }
        
    #     # รัน agent        
    #     result = agent_executor.invoke(inputs)
        
    #     # ดึงคำตอบจาก messages
    #     if "messages" in result:
    #         # ข้อความสุดท้ายคือคำตอบ
    #         last_message = result["messages"][-1]
    #         answer = last_message.content
            
    #         if verbose:
    #             print(f"\n{'='*60}")
    #             print(f"💭 Agent Thinking Process:")
    #             print(f"{'='*60}")
    #             for i, msg in enumerate(result["messages"]):
    #                 msg_type = type(msg).__name__
    #                 content = msg.content[:200] + "..." if len(msg.content) > 200 else msg.content
    #                 print(f"\n[{i+1}] {msg_type}:")
    #                 print(content)
    #     else:
    #         answer = str(result)
        
    #     return {
    #         'input': query,
    #         'output': answer
    #     }
        
    # except Exception as e:
    #     import traceback
    #     error_details = traceback.format_exc()
    #     print(f"\n❌ Error: {str(e)}")
    #     print(f"\nDetails:\n{error_details}")
        
    #     return {
    #         'input': query,
    #         'output': f"Error: {str(e)}"
    #     }


# --- ส่วนสำหรับทดสอบ (Test Block) ---
if __name__ == "__main__":
    """
    ทดสอบ Agent
    """
    print("=" * 60)
    print("🧪 ทดสอบ LangGraph Agent (LangChain v1.0.3)")
    print("=" * 60)
    
    try:
        agent = get_agent_executor()
        
        if agent:
            # --- Test 1: WEO Question ---            
            # TODO: (Class 4) ให้นักเรียน uncomment บรรทัดล่าง
            # print("\n" + "=" * 60)
            # print("📊 [Test 1] คำถามเกี่ยวกับ WEO")
            # print("=" * 60)
            # q1 = "What is the 2025 GDP growth forecast for Thailand?"
            # result1 = run_agent(agent, q1)
            # print(f"\n✅ Final Answer:\n{result1['output']}\n")

            # --- Test 2: Math Question ---
            # TODO: (Class 4) ให้นักเรียน uncomment บรรทัดล่าง            
            # print("\n" + "=" * 60)
            # print("🔢 [Test 2] คำถามคณิตศาสตร์")
            # print("=" * 60)
            # q2 = "Calculate 4.5 multiplied by 2"
            # result2 = run_agent(agent, q2)
            # print(f"\n✅ Final Answer:\n{result2['output']}\n")

            # --- Test 3: Off-topic ---
            # TODO: (Class 4) ให้นักเรียน uncomment บรรทัดล่าง
            # print("\n" + "=" * 60)
            # print("🚫 [Test 3] คำถาม Off-topic")
            # print("=" * 60)
            # q3 = "What is the weather in Bangkok today?"
            # result3 = run_agent(agent, q3)
            # print(f"\n✅ Final Answer:\n{result3['output']}\n")
            
            print("=" * 60)
            print("🎉 ทดสอบเสร็จสมบูรณ์!")
            print("=" * 60)
        else:
            print("❌ ไม่สามารถสร้าง Agent ได้")
            
    except Exception as e:
        print(f"\n❌ เกิดข้อผิดพลาด: {str(e)}")
        import traceback
        traceback.print_exc()
        
        print("\n💡 ตรวจสอบ:")
        print("1. Ollama กำลังรันอยู่: ollama serve")
        print("2. มีโมเดล llama3.2:3b: ollama pull llama3.2:3b")
        print("3. มีไฟล์ retriever.py และ vector store")
        print("4. มีแพคเกจครบ")