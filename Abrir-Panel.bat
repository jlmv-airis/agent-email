@echo off
title Servidor del Panel - Agente de Email AI
echo.
echo --- INICIANDO INTERFAZ DE USUARIO (PYTHON) ---
echo.
echo El panel estara disponible en: http://localhost:8000/login.html
echo (Asegurate de que n8n este corriendo en http://localhost:5678)
echo.

python server.py
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ERROR: No se pudo iniciar el servidor de Python. 
    echo Asegurate de tener Python instalado y agregado al PATH.
    echo Intentando con el metodo alternativo (PowerShell)...
    echo.
    powershell -NoProfile -ExecutionPolicy Bypass -Command "Start-Process 'login.html'"
)
pause
