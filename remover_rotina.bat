@echo off
setlocal
chcp 65001 > nul
title Remover Rotina Diaria - Agente de Noticias DIO

echo ======================================================================
echo    REMOVENDO ROTINA AUTOMATICA DO AGENDADOR DE TAREFAS
echo ======================================================================
echo.

powershell.exe -NoProfile -Command "Unregister-ScheduledTask -TaskName 'AgenteNoticiasDIO' -Confirm:$false -ErrorAction SilentlyContinue"

echo [OK] A rotina automatica foi removida com sucesso.
echo.
pause
