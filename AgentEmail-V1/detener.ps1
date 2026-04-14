# ==============================================================================
#  AGENT EMAIL AIRIS V1 - SCRIPT DE DETENCIÓN
#
#  Uso:
#    .\detener.ps1
#
#  Opciones:
#    -Force   Detiene los procesos sin pedir confirmación.
# ==============================================================================

param(
    [switch]$Force
)

$ErrorActionPreference = "Continue"

Write-Host "=========================================="
Write-Host "  AGENT EMAIL AIRIS V1 - Detener Servicios"
Write-Host "=========================================="
Write-Host ""

# --- Búsqueda de Procesos ---

# Busca procesos Python que estén ejecutando el servidor de este proyecto.
# Esto es más seguro que detener todos los procesos 'python.exe'.
$pythonProcesses = Get-CimInstance Win32_Process -Filter "Name = 'python.exe' AND CommandLine LIKE '%server.py%'"

if ($null -eq $pythonProcesses -or $pythonProcesses.Count -eq 0) {
    Write-Host "✅ No se encontraron procesos del servidor (server.py) ejecutándose." -ForegroundColor Green
    Write-Host ""
    exit 0
}

# --- Confirmación ---

Write-Host "📊 Procesos del servidor detectados:" -ForegroundColor Yellow
Write-Host ""

foreach ($process in $pythonProcesses) {
    Write-Host "  -> PID: $($process.ProcessId) | Comando: $($process.CommandLine)" -ForegroundColor Gray
}
Write-Host ""

if (-not $Force) {
    $response = Read-Host "¿Deseas detener estos procesos? (s/n)"
    if ($response -notmatch '^[sS]') {
        Write-Host "⚠️ Operación cancelada." -ForegroundColor Yellow
        exit 0
    }
}

# --- Detención de Procesos ---

Write-Host ""
Write-Host "==> Deteniendo servicios..." -ForegroundColor Cyan

foreach ($process in $pythonProcesses) {
    try {
        Stop-Process -Id $process.ProcessId -Force
        Write-Host "  -> Proceso $($process.ProcessId) detenido." -ForegroundColor Green
    } catch {
        Write-Host "  -> ❌ Error al detener el proceso $($process.ProcessId): $_" -ForegroundColor Red
    }
}

# --- Verificación Final ---

Write-Host ""
Start-Sleep -Seconds 1
$remainingProcesses = Get-CimInstance Win32_Process -Filter "Name = 'python.exe' AND CommandLine LIKE '%server.py%'"

if ($null -eq $remainingProcesses -or $remainingProcesses.Count -eq 0) {
    Write-Host "=========================================="
    Write-Host "✅ ¡SERVICIOS DETENIDOS CORRECTAMENTE!" -ForegroundColor Green
    Write-Host "=========================================="
} else {
    Write-Warning "⚠️ Aún quedan procesos del servidor ejecutándose."
}

Write-Host ""
