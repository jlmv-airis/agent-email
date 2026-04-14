@echo off
chcp 65001 >nul
title Agent Email AIRIS V1 - Detener Servicios
color 0C

echo.
echo ==========================================
echo   AGENT EMAIL AIRIS V1
echo   Deteniendo Servicios
echo ==========================================
echo.

REM Buscar procesos python
tasklist /FI "IMAGENAME eq python.exe" 2>NUL | find /I /N "python.exe">NUL
if "%ERRORLEVEL%"=="0" (
    echo [INFO] Procesos Python detectados:
    echo.
    tasklist /FI "IMAGENAME eq python.exe" /V | find "python.exe"
    echo.
    echo [!] Deteniendo servicios...
    echo.
    
    REM Detener todos los procesos python
    taskkill /IM python.exe /F /T
    
    if "%ERRORLEVEL%"=="0" (
        echo.
        echo [OK] Procesos detenidos correctamente
    ) else (
        echo.
        echo [ERROR] No se pudieron detener los procesos
    )
) else (
    echo [INFO] No hay procesos Python ejecutándose
)

echo.
echo ==========================================
echo   SERVICIOS DETENIDOS
echo ==========================================
echo.

timeout /t 3 /nobreak
