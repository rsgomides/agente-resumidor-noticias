@echo off
setlocal
chcp 65001 > nul
cd /d "%~dp0"

:: Executa o agente de notícias
if exist ".venv\Scripts\python.exe" (
    ".venv\Scripts\python.exe" main.py
) else (
    python main.py
)
