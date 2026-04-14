param(
    [switch]$Verbose
)

$ErrorActionPreference = "SilentlyContinue"

Write-Host ""
Write-Host "=========================================="
Write-Host "  AGENT EMAIL AIRIS V1"
Write-Host "  Sistema de Diagnostico"
Write-Host "=========================================="
Write-Host ""

$projectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$venvDir = Join-Path $projectRoot ".venv"
$venvPython = Join-Path $venvDir "Scripts\python.exe"
$backendDir = Join-Path $projectRoot "backend"
$logsDir = Join-Path $backendDir "logs"
$logFile = Join-Path $logsDir "agent-email.log"
$envFile = Join-Path $projectRoot ".env"
$dbFile = Join-Path $projectRoot "database\agent_email.db"

Write-Host "[INFO] INFORMACION DEL SISTEMA" -ForegroundColor Cyan
Write-Host "=========================================="
Write-Host ""

# Ruta del proyecto
Write-Host "[PATH] Rutas del Proyecto:"
Write-Host "       Raiz: $projectRoot" -ForegroundColor Gray
Write-Host "       Backend: $backendDir" -ForegroundColor Gray
Write-Host "       Logs: $logsDir" -ForegroundColor Gray
Write-Host ""

# Entorno Virtual
Write-Host "[PYTHON] Entorno Virtual:"
if (Test-Path $venvPython) {
    Write-Host "         OK - Entorno virtual encontrado" -ForegroundColor Green
    $pythonVersion = & $venvPython --version 2>&1
    Write-Host "         Version: $pythonVersion" -ForegroundColor Gray
} else {
    Write-Host "         ERROR - Entorno virtual NO encontrado" -ForegroundColor Red
}
Write-Host ""

# Estado del Servidor
Write-Host "[SERVER] Estado del Servidor:"
$pythonProcesses = Get-Process -Name python -ErrorAction SilentlyContinue
if ($null -ne $pythonProcesses) {
    Write-Host "         OK - Procesos Python ejecutandose" -ForegroundColor Green
    if ($pythonProcesses -is [array]) {
        Write-Host "         Cantidad: $($pythonProcesses.Count) procesos" -ForegroundColor Gray
        foreach ($proc in $pythonProcesses) {
            $mem = [math]::Round($proc.WorkingSet / 1MB, 2)
            Write-Host "           PID: $($proc.Id) | Memoria: $mem MB" -ForegroundColor Gray
        }
    } else {
        Write-Host "         Cantidad: 1 proceso" -ForegroundColor Gray
        $mem = [math]::Round($pythonProcesses.WorkingSet / 1MB, 2)
        Write-Host "           PID: $($pythonProcesses.Id) | Memoria: $mem MB" -ForegroundColor Gray
    }
} else {
    Write-Host "         WARNING - No hay procesos Python ejecutandose" -ForegroundColor Yellow
}
Write-Host ""

# Conectividad
Write-Host "[WEB] Conectividad:"
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8000" -UseBasicParsing -TimeoutSec 2 -ErrorAction SilentlyContinue
    if ($response.StatusCode -eq 200) {
        Write-Host "       OK - Servidor respondiendo (HTTP 200)" -ForegroundColor Green
        Write-Host "       URL: http://localhost:8000" -ForegroundColor Gray
    }
} catch {
    Write-Host "       ERROR - Servidor NO respondiendo" -ForegroundColor Red
}
Write-Host ""

# Archivos importantes
Write-Host "[FILES] Archivos Importantes:"
Write-Host "        .env: $(if (Test-Path $envFile) { 'OK' } else { 'FALTA' })" -ForegroundColor Gray
Write-Host "        Base de Datos: $(if (Test-Path $dbFile) { 'OK' } else { 'FALTA' })" -ForegroundColor Gray
Write-Host "        Logs Dir: $(if (Test-Path $logsDir) { 'OK' } else { 'FALTA' })" -ForegroundColor Gray
if (Test-Path $logFile) {
    $logSize = (Get-Item $logFile).Length / 1KB
    Write-Host "        Log Size: $([math]::Round($logSize, 2)) KB" -ForegroundColor Gray
}
Write-Host ""

# Dependencias
Write-Host "[DEPS] Dependencias Instaladas:"
if (Test-Path $venvPython) {
    $packages = & $venvPython -m pip list --quiet 2>&1 | Select-Object -Skip 2
    $packageCount = ($packages | Measure-Object -Line).Lines
    Write-Host "       Total: $packageCount paquetes" -ForegroundColor Gray
    
    $requiredPackages = @("flask", "flask-cors", "pyjwt", "cryptography", "imap-tools", "python-json-logger")
    Write-Host ""
    Write-Host "       Paquetes Requeridos:"
    foreach ($pkg in $requiredPackages) {
        $installed = $packages -match $pkg | Select-Object -First 1
        if ($installed) {
            Write-Host "         OK - $installed" -ForegroundColor Green
        } else {
            Write-Host "         FALTA - $pkg" -ForegroundColor Red
        }
    }
} else {
    Write-Host "       ERROR - Entorno virtual no encontrado" -ForegroundColor Red
}
Write-Host ""

# Últimas líneas del log
if (Test-Path $logFile) {
    Write-Host "[LOGS] Ultimas Lineas del Log:" -ForegroundColor Cyan
    Write-Host "=========================================="
    Get-Content $logFile -Tail 10 | ForEach-Object { Write-Host "        $_" -ForegroundColor Gray }
    Write-Host ""
}

Write-Host "=========================================="
Write-Host "OK - DIAGNOSTICO COMPLETO" -ForegroundColor Green
Write-Host "==========================================" 
