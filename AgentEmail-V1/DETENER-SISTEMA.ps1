param(
    [switch]$Force
)

$ErrorActionPreference = "Continue"

Write-Host ""
Write-Host "=========================================="
Write-Host "  AGENT EMAIL AIRIS V1"
Write-Host "  Deteniendo Servicios"
Write-Host "=========================================="
Write-Host ""

# Obtener todos los procesos de Python
$pythonProcesses = Get-Process -Name python -ErrorAction SilentlyContinue

if ($null -eq $pythonProcesses) {
    Write-Host "ℹ️  No hay procesos Python ejecutándose." -ForegroundColor Cyan
    Write-Host ""
    exit 0
}

# Convertir a array si solo hay un proceso
if ($pythonProcesses -isnot [array]) {
    $pythonProcesses = @($pythonProcesses)
}

Write-Host "📊 Procesos Python detectados:" -ForegroundColor Yellow
Write-Host ""

foreach ($process in $pythonProcesses) {
    $cmdLine = (Get-WmiObject Win32_Process -Filter "ProcessId = $($process.Id)").CommandLine
    Write-Host "  PID: $($process.Id) | Memoria: $([math]::Round($process.WorkingSet / 1MB, 2))MB" -ForegroundColor Gray
    Write-Host "  Comando: $cmdLine" -ForegroundColor Gray
    Write-Host ""
}

if (-not $Force) {
    $response = Read-Host "¿Deseas detener los procesos? (s/n)"
    if ($response -ne 's') {
        Write-Host ""
        Write-Host "⚠️  Operación cancelada" -ForegroundColor Yellow
        Write-Host ""
        exit 0
    }
}

Write-Host ""
Write-Host "Deteniendo servicios..." -ForegroundColor Cyan

foreach ($process in $pythonProcesses) {
    try {
        Stop-Process -Id $process.Id -Force
        Write-Host "✅ Proceso $($process.Id) detenido" -ForegroundColor Green
    } catch {
        Write-Host "❌ Error deteniendo proceso $($process.Id): $_" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "=========================================="
Write-Host "✅ SERVICIOS DETENIDOS" -ForegroundColor Green
Write-Host "=========================================="
Write-Host ""

# Verificar que todos se detuvo
Start-Sleep -Seconds 1
$remainingProcesses = Get-Process -Name python -ErrorAction SilentlyContinue
if ($null -eq $remainingProcesses) {
    Write-Host "✅ Todos los procesos han sido detenidos correctamente" -ForegroundColor Green
} else {
    Write-Host "⚠️  Aún hay procesos Python ejecutándose" -ForegroundColor Yellow
}

Write-Host ""
