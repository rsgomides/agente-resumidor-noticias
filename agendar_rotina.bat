@echo off
setlocal
chcp 65001 > nul
title Agendar Rotina Diaria - Agente de Noticias DIO

echo ======================================================================
echo    CONFIGURANDO ROTINA AUTOMATICA DIARIA AS 13:00 (BRASILIA)
echo ======================================================================
echo.

powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0agendar_rotina.ps1"

echo.
pause
