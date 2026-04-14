@echo off
title Agent Email AIRIS V1 - Sistema de Gestion
echo ==========================================
echo   INICIANDO AGENT EMAIL AIRIS V1
echo ==========================================
echo.
echo 1. Abriendo panel en el navegador...
start http://localhost:8000
echo 2. Iniciando servidor backend (Flask)...
cd backend
python server.py
pause