# REPO: weo-rag-chatbot
# FILE: app.py
# =========================================
# บทบาทไฟล์นี้ (UI ตัวอย่างด้วย Streamlit)
# - อินเทอร์เฟซแชตง่าย ๆ เพื่อคุยกับ agent.py
# - เก็บประวัติข้อความใน session_state
# - โค้ดนี้ตั้งใจให้สั้นและอ่านง่าย เหมาะกับการสอน "โฟลว์งาน" มากกว่า UI สวยงาม
#
# จุดฝึก (TODO):
# - ทำปุ่มเปิด/ปิดการแสดง citation แยกบรรทัด
# - ทำ streaming token-by-token (ขั้นสูง)
# - ปรับ Theme/เค้าโครง UI
# =========================================

import streamlit as st
from agent import answer

st.set_page_config(page_title="WEO RAG Chat", page_icon="📘", layout="centered")
st.title("WEO RAG Chatbot (Student Starter)")
st.caption("LLM: gemma3:1b via Ollama • Vector DB: Qdrant Cloud • Source: data/weo.pdf")

# เก็บบทสนทนาไว้ใน state (อยู่แค่รอบรัน/แท็บนี้)
if "messages" not in st.session_state:
    st.session_state.messages = []

# แสดงประวัติสนทนาเดิม
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

# ช่องพิมพ์คำถาม
q = st.chat_input("ถามเกี่ยวกับ WEO ได้เลย (ต้องอ้างอิง [p.X])")
if q:
    # แสดงคำถามฝั่งผู้ใช้
    st.session_state.messages.append({"role": "user", "content": q})
    with st.chat_message("user"):
        st.markdown(q)

    # เรียก agent ตอบ
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            ans = answer(q)
        st.markdown(ans)

    # เก็บคำตอบไว้ด้วย
    st.session_state.messages.append({"role": "assistant", "content": ans})
