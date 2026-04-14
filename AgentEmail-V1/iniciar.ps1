# ==============================================================================
#  AGENT EMAIL AIRIS V1 - SCRIPT DE INICIO
#
#  Uso:
#    .\iniciar.ps1
#
#  Opciones:
#    -SkipInstall    Omite la instalación de dependencias de Python.
#    -Port <numero>  Especifica el puerto para la aplicación (ej. 8001).
# ==============================================================================

param(
    [switch]$SkipInstall,
    [ValidateRange(1, 65535)]
    [int]$Port = 8000
)

$ErrorActionPreference = "Stop"

# --- Funciones de Ayuda ---

function Write-Step {
    param([string]$Message)
    Write-Host "==> $Message" -ForegroundColor Cyan
}

function Assert-Command {
    param([string]$CommandName)
    if (-not (Get-Command $CommandName -ErrorAction SilentlyContinue)) {
        throw "Comando '$CommandName' no encontrado. Asegúrate de que esté en tu PATH."
    }
}

function Get-PortOwnerInfo {
    param([int]$Port)
    try {
        $connection = Get-NetTCPConnection -LocalPort $Port -State Listen -ErrorAction SilentlyContinue | Select-Object -First 1
        if (-not $connection) {
            return $null
        }

        $process = Get-Process -Id $connection.OwningProcess -ErrorAction SilentlyContinue
        if ($process) {
            return @{
                Pid = $connection.OwningProcess
                Name = $process.ProcessName
            }
        }
        return @{ Pid = $connection.OwningProcess; Name = "Desconocido" }
    }
    catch {
        Write-Warning "No se pudo verificar el puerto $Port. Puede que necesites permisos de administrador."
        return $null
    }
}

# --- Inicialización ---

$projectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path | Resolve-Path
$backendDir = Join-Path $projectRoot "backend"
$logsDir = Join-Path $backendDir "logs"
$venvDir = Join-Path $projectRoot ".venv"
$venvPython = Join-Path $venvDir "Scripts\python.exe"
$requirementsFile = Join-Path $projectRoot "requirements.txt"
$appPort = $Port

Write-Host "=========================================="
Write-Host "  AGENT EMAIL AIRIS V1 - INICIO LOCAL"
Write-Host "=========================================="
Write-Host "Puerto de la aplicación: $appPort"
Write-Host "Fecha/Hora: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
Write-Host ""

Assert-Command -CommandName "python"
Set-Location $projectRoot

# --- Preparación del Entorno ---

if (-not (Test-Path $logsDir)) {
    Write-Step "Creando directorio de logs en '$logsDir'"
    New-Item -ItemType Directory -Path $logsDir | Out-Null
}

if (-not (Test-Path $venvPython)) {
    Write-Step "Creando entorno virtual en '.venv'. Esto puede tardar un momento..."
    python -m venv .venv
    if (-not (Test-Path $venvPython)) {
        throw "No se pudo crear el entorno virtual en '$venvDir'."
    }
    Write-Host "Entorno virtual creado." -ForegroundColor Green
}

if (-not $SkipInstall) {
    Write-Step "Instalando/actualizando dependencias (puede tardar varios minutos)..."
    
    Write-Host "  -> Actualizando pip..."
    & $venvPython -m pip install --upgrade pip --quiet --disable-pip-version-check
    
    if (Test-Path $requirementsFile) {
        Write-Host "  -> Instalando desde requirements.txt..."
        & $venvPython -m pip install -r $requirementsFile --quiet --disable-pip-version-check
    } else {
        Write-Warning "No se encontró 'requirements.txt'."
    }
    
    Write-Host "  -> Instalando paquetes adicionales (logging, limiter, testing)..."
    & $venvPython -m pip install python-json-logger flask-limiter pytest pytest-cov --quiet --disable-pip-version-check
    
    Write-Host "Instalación de dependencias completada." -ForegroundColor Green
} else {
    Write-Host "⚡ Omitiendo instalación de dependencias." -ForegroundColor Yellow
}

# --- Verificación del Puerto ---

if (-not (Test-Path $backendDir)) {
    throw "❌ No se encontró el directorio 'backend' en '$projectRoot'."
}

$portOwner = Get-PortOwnerInfo -Port $appPort
if ($portOwner) {
    Write-Warning "El puerto $appPort ya está en uso por el proceso '$($portOwner.Name)' (PID: $($portOwner.Pid))."
    $response = Read-Host "¿Deseas intentar con un puerto diferente? (s/n)"
    if ($response -match '^[sS]') {
        $newPort = Read-Host "Ingresa el nuevo número de puerto (1-65535)"
        if ($newPort -match '^\d+$' -and [int]$newPort -ge 1 -and [int]$newPort -le 65535) {
            $appPort = [int]$newPort
            Write-Host "Usando nuevo puerto: $appPort" -ForegroundColor Green
        } else {
            throw "Puerto inválido. Abortando."
        }
    } else {
        throw "Abortando. Libera el puerto $appPort o reinicia con un puerto diferente."
    }
}

$env:PORT = "$appPort"

# --- Arranque de Servicios ---

Write-Host ""
Write-Step "Iniciando servidor Flask en segundo plano..."
$env:PYTHONUNBUFFERED = "1"

$serverProcess = Start-Process -FilePath $venvPython `
    -ArgumentList "server.py" `
    -WorkingDirectory $backendDir `
    -WindowStyle Hidden `
    -PassThru

if ($null -eq $serverProcess) {
    throw "Error al iniciar el servidor Flask. Revisa los logs para más detalles."
}

Write-Host "[OK] Proceso del servidor iniciado (PID: $($serverProcess.Id))" -ForegroundColor Green

# --- Verificación de Salud del Servidor ---

Write-Step "Esperando que el servidor esté listo (máx. 20 segundos)..."
$healthCheckUrl = "http://localhost:$appPort/api/status"
$maxAttempts = 20
$serverReady = $false

foreach ($attempt in 1..$maxAttempts) {
    try {
        $response = Invoke-WebRequest -Uri $healthCheckUrl -UseBasicParsing -TimeoutSec 1 -ErrorAction SilentlyContinue
        if ($response.StatusCode -eq 200) {
            $serverReady = $true
            break
        }
    }
    catch { } # Ignorar errores de conexión
    
    Write-Host "  Intento $attempt/$maxAttempts..." -ForegroundColor Gray
    Start-Sleep -Seconds 1
}

# --- Finalización ---

Write-Host ""
if ($serverReady) {
    Write-Host "=================================================" -ForegroundColor Green
    Write-Host "✅ ¡SISTEMA INICIADO CORRECTAMENTE!" -ForegroundColor Green
    Write-Host "=================================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "  -> URL de la aplicación: http://localhost:$appPort" -ForegroundColor Cyan
    Write-Host "  -> Logs del servidor: $logsDir\agent-email.log" -ForegroundColor Cyan
    Write-Host "  -> Para detener el sistema, ejecuta: .\detener.ps1" -ForegroundColor Yellow
    Write-Host ""
    
    Start-Process "http://localhost:$appPort"
} else {
    Write-Warning "El servidor no respondió a tiempo."
    Write-Warning "Puede que aún se esté iniciando. Revisa los logs para más detalles:"
    Write-Warning "$logsDir\agent-email.log"
}

Write-Host ""
Write-Host "Este script ha finalizado. El servidor continúa en segundo plano." -ForegroundColor Gray
Write-Host ""
