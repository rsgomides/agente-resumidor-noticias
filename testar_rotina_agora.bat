@echo off
setlocal
chcp 65001 > nul
title Testar Rotina Agendada Agora - Agente de Noticias DIO

echo ======================================================================
echo    TESTANDO EXECUCAO DA ROTINA AGENDADA AGORA
echo ======================================================================
echo.
echo [*] Disparando a tarefa agendada 'AgenteNoticiasDIO' em segundo plano...

powershell.exe -NoProfile -Command "Start-ScheduledTask -TaskName 'AgenteNoticiasDIO'"

echo.
echo [OK] Tarefa iniciada em segundo plano!
echo Em poucos segundos, o agente finalizara a curadoria e abrira o navegador.
echo.
pause
