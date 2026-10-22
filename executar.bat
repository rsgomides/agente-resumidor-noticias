@echo off
setlocal
chcp 65001 > nul
title Agente Resumidor de Noticias de IA - DIO

echo ======================================================================
echo    [AGENTE DE IA] CURADORIA DIARIA DE NOTICIAS DE TECNOLOGIA
echo ======================================================================
echo.

cd /d "%~dp0"

:: 1. Verifica se o ambiente virtual existe
if not exist ".venv\Scripts\python.exe" (
    echo [!] Ambiente virtual nao encontrado. Criando .venv e instalando dependencias...
    python -m venv .venv
    .venv\Scripts\pip install -r requirements.txt
    if errorlevel 1 (
        echo.
        echo [ERRO] Falha ao configurar o ambiente virtual.
        pause
        exit /b 1
    )
)

:: 2. Executa o Agente com o Python do ambiente virtual
echo [*] Executando o agente de IA...
echo [*] Monitorando feeds RSS e gerando relatorio HTML/Markdown...
echo.

.venv\Scripts\python.exe main.py

if errorlevel 1 (
    echo.
    echo ======================================================================
    echo  [ERRO] Ocorreu uma falha durante a execucao do agente.
    echo ======================================================================
    pause
    exit /b 1
)

echo.
echo ======================================================================
echo  [OK] Processo concluido com sucesso!
echo  A pagina de noticias foi aberta no seu navegador padrao.
echo ======================================================================
echo.
pause
