# REPO: weo-rag-chatbot
# FILE: run_ollama_windows.cmd
@echo off
REM ---------------------------------------------------------
REM สคริปต์ช่วยนักเรียนสาย Windows:
REM 1) ดึงโมเดล LLM gemma3:1b มารันบนเครื่องผ่าน Ollama
REM 2) เตือนให้เปิดบริการ Ollama ก่อนใช้งานโปรเจกต์นี้
REM ---------------------------------------------------------

echo Pulling model gemma3:1b (one-time)...
ollama pull gemma3:1b

echo.
echo Done. Now start the Ollama service in another terminal:
echo    ollama serve
echo.
pause
