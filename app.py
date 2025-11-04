import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage

# Import agent executor ของเรา
# (ไฟล์ agent.py ต้องมีฟังก์ชัน get_agent_executor() ที่สมบูรณ์)
from agent import get_agent_executor

# === 1. ตั้งค่าหน้า Streamlit (Class 4, Slide 9) ===
st.set_page_config(page_title="WEO Chatbot", layout="centered")
st.title("WEO RAG Chatbot 🤖")

# === 2. สร้าง Agent Executor ===
# เราสร้าง Agent Executor เพียงครั้งเดียวและเก็บไว้ใน cache ของ Streamlit
# เพื่อให้ไม่ต้องสร้างใหม่ทุกครั้งที่ User พิมพ์
@st.cache_resource
def load_agent_executor():
    """
    โหลด Agent Executor และเก็บใน cache
    """
    return get_agent_executor()

# TODO: (Class 4) ให้นักเรียน uncomment บรรทัดล่างนี้
# (หลังจากที่ agent.py พร้อมใช้งานแล้ว)
# agent_executor = load_agent_executor()

# === 3. จัดการ Chat History (Class 4, Slide 10) ===

# Streamlit จะ "รันใหม่ทั้งไฟล์" ทุกครั้งที่มีการโต้ตอบ
# เราจึงต้องเก็บประวัติแชท (Chat History) ไว้ใน st.session_state
if "messages" not in st.session_state:
    st.session_state.messages = [] # (เก็บ {"role": "user", "content": "..."})

# แสดงประวัติแชทที่ผ่านมา (Display chat messages)
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"]) # ใช้ markdown เพื่อให้ link/citation แสดงผลสวยงาม

# === 4. รับ Input และเรียก Agent (Class 4, Slide 11) ===

# รับ Input จาก User (ช่องพิมพ์จะอยู่ด้านล่าง)
if prompt := st.chat_input("Ask about WEO..."):
    
    # 4.1. เพิ่มคำถาม User ไปยัง History และแสดงผล
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 4.2. เรียก Agent เพื่อประมวลผลคำตอบ
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            
            # TODO: (Class 4) ให้นักเรียน uncomment ส่วนนี้
            
            # --- ส่วนแปลง History (สำคัญ!) ---
            # Agent ของเรา (Class 3) รับ history ในรูปแบบ [HumanMessage, AIMessage]
            # แต่ st.session_state เก็บเป็น [dict, dict]
            # เราจึงต้องแปลงก่อนส่ง
            # chat_history_for_agent = []
            # for msg in st.session_state.messages[:-1]: # (เอาทุกอัน *ยกเว้น* คำถามล่าสุด)
            #     if msg["role"] == "user":
            #         chat_history_for_agent.append(HumanMessage(content=msg["content"]))
            #     else:
            #         chat_history_for_agent.append(AIMessage(content=msg["content"]))
            # ---------------------------------
            
            # print(f"--- [App] Sending to agent: {prompt} ---")
            # print(f"--- [App] History size: {len(chat_history_for_agent)} ---")

            # *** เรียก Agent ***
            # response = agent_executor.invoke({
            #     "input": prompt,
            #     "chat_history": chat_history_for_agent
            # })
            
            # response_text = response['output']
            
            # (ใส่ text จำลองไว้ก่อน จนกว่า TODO ข้างบนจะเสร็จ)
            response_text = "TODO: Agent is not connected yet."
            
            st.markdown(response_text)
            
            # (สำคัญมาก!) ให้นักเรียนดูที่ "Terminal" ที่รัน streamlit
            # ถ้า agent_executor มี verbose=True, เราจะเห็น "ความคิด" (ReAct loop) ของ Agent ที่นั่น

    # 4.3. เพิ่มคำตอบของ Bot ไปยัง History
    st.session_state.messages.append({"role": "assistant", "content": response_text})

