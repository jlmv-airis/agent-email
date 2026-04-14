@echo off
chcp 65001 >nul
title Agent Email AIRIS V1 - Sistema de Gestion
color 0A

echo.
echo ==========================================
echo   AGENT EMAIL AIRIS V1
echo   Sistema de Gestion Unificado
echo ==========================================
echo.
echo [%date% %time%] Iniciando servicios...
echo.

rem Define project paths
set PROJECT_ROOT=%~dp0
set VENV_DIR=%PROJECT_ROOT%.venv
set VENV_PYTHON=%VENV_DIR%\Scripts\python.exe
set BACKEND_DIR=%PROJECT_ROOT%backend
set LOGS_DIR=%BACKEND_DIR%\logs
set PORT=8000

rem Check if virtual environment exists
if not exist "%VENV_PYTHON%" (
    echo [ERROR] Entorno virtual no encontrado.
    echo Ejecuta INICIAR-SISTEMA.ps1 primero desde PowerShell.
    echo.
    pause
    exit /b 1
)

rem Create logs directory if it doesn't exist
if not exist "%LOGS_DIR%" (
    echo [INFO] Creando directorio de logs...
    mkdir "%LOGS_DIR%" >nul
)

rem Ensure .env file exists with SECRET_KEY and PORT
set ENV_FILE=%PROJECT_ROOT%.env
if not exist "%ENV_FILE%" (
    echo.
    echo [INFO] Generando archivo .env con configuracion...
    for /f "delims=" %%i in ('"%VENV_PYTHON%" -c "import secrets; print(secrets.token_hex(32))"') do set SECRET_KEY_GEN=%%i
    (
        echo SECRET_KEY=%SECRET_KEY_GEN%
        echo PORT=%PORT%
        echo ENVIRONMENT=production
    ) > "%ENV_FILE%"
    echo [OK] Archivo .env creado exitosamente
    echo.
) else (
    rem Ensure PORT is in .env if it exists
    findstr /B /C:"PORT=" "%ENV_FILE%" >nul || echo PORT=%PORT%>> "%ENV_FILE%"
)

echo.
echo ==========================================
echo   INICIANDO SERVIDOR FLASK
echo ==========================================
echo.
echo URL: http://localhost:%PORT%
echo Credenciales: admin@airis.com / admin123
echo Logs: %LOGS_DIR%\agent-email.log
echo.
echo Abriendo navegador en 3 segundos...
timeout /t 3 /nobreak

start http://localhost:%PORT%

echo [INFO] Iniciando servidor Flask en segundo plano...
echo.

cd /d "%BACKEND_DIR%"
set "PORT=%PORT%"
set "PYTHONUNBUFFERED=1"

REM Iniciar servidor con salida redirigida a log
start "" /min "%VENV_PYTHON%" server.py

echo [OK] Servidor iniciado (PID: detectar en Task Manager)
echo.
echo ==========================================
echo   ESTADO: SERVICIOS ACTIVOS
echo ==========================================
echo.
echo [!] Para detener el servidor:
echo     1. Abre Task Manager (Ctrl+Shift+Esc)
echo     2. Busca "python.exe"
echo     3. Click derecho ^> Finalizar tarea
echo.
echo [!] O ejecuta en PowerShell:
echo     Get-Process python ^| Stop-Process -Force
echo.

timeout /t 5 /nobreak