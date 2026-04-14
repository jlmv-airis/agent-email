param(
    [switch]$SkipInstall,
    [ValidateRange(1, 65535)]
    [int]$Port = 8000
)

$ErrorActionPreference = "Stop"

function Write-Step {
    param([string]$Message)
    Write-Host "==> $Message" -ForegroundColor Cyan
}

function Assert-Command {
    param([string]$CommandName)
    if (-not (Get-Command $CommandName -ErrorAction SilentlyContinue)) {
        throw "No se encontro '$CommandName' en PATH. Instala Python 3.10+ y vuelve a intentar."
    }
}

function Get-PortOwnerInfo {
    param([int]$Port)
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

    return @{
        Pid = $connection.OwningProcess
        Name = "desconocido"
    }
}

$projectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$backendDir = Join-Path $projectRoot "backend"
$logsDir = Join-Path $backendDir "logs"
$venvDir = Join-Path $projectRoot ".venv"
$venvPython = Join-Path $venvDir "Scripts\python.exe"
$requirementsFile = Join-Path $projectRoot "requirements.txt"
$appPort = $Port

Write-Host "=========================================="
Write-Host "  AGENT EMAIL AIRIS V1 - INICIO LOCAL"
Write-Host "=========================================="
Write-Host "Puerto configurado: $appPort"
Write-Host "Fecha/Hora: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
Write-Host ""

Assert-Command -CommandName "python"

Set-Location $projectRoot

# Crear carpeta de logs si no existe
if (-not (Test-Path $logsDir)) {
    Write-Step "Creando directorio de logs"
    New-Item -ItemType Directory -Path $logsDir | Out-Null
}

if (-not (Test-Path $venvPython)) {
    Write-Step "Creando entorno virtual (.venv)"
    python -m venv .venv
}

if (-not (Test-Path $venvPython)) {
    throw "No se pudo crear el entorno virtual en '$venvDir'."
}

if (-not $SkipInstall) {
    Write-Step "Actualizando pip"
    & $venvPython -m pip install --upgrade pip --quiet

    Write-Step "Instalando dependencias desde requirements.txt y extras"
    if (Test-Path $requirementsFile) {
        & $venvPython -m pip install -r $requirementsFile --quiet
    } else {
        Write-Host "Aviso: no existe requirements.txt" -ForegroundColor Yellow
    }

    # Instalar paquetes adicionales necesarios
    Write-Step "Instalando paquetes adicionales requeridos"
    & $venvPython -m pip install python-json-logger flask-limiter pytest pytest-cov --quiet
} else {
    Write-Host "⚡ SkipInstall activo: se omite instalacion de paquetes" -ForegroundColor Yellow
}

if (-not (Test-Path $backendDir)) {
    throw "❌ No se encontro la carpeta backend en '$projectRoot'."
}

$portOwner = Get-PortOwnerInfo -Port $appPort
if ($portOwner) {
    Write-Host "⚠️  El puerto $appPort ya esta en uso" -ForegroundColor Yellow
    Write-Host "   PID: $($portOwner.Pid) | Proceso: $($portOwner.Name)"
    $response = Read-Host "¿Deseas usar un puerto diferente? (s/n)"
    if ($response -eq 's') {
        $newPort = Read-Host "Ingresa el nuevo puerto (1-65535)"
        $appPort = [int]$newPort
        $env:PORT = "$appPort"
    } else {
        throw "❌ No es posible continuar con el puerto $appPort en uso."
    }
} else {
    $env:PORT = "$appPort"
}

Write-Host ""
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Step "🚀 Iniciando servicios..."
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host ""

# Iniciar servidor Flask en background
Write-Step "Iniciando servidor Flask en puerto $appPort"
$serverProcess = Start-Process -FilePath $venvPython `
    -ArgumentList "server.py" `
    -WorkingDirectory $backendDir `
    -WindowStyle Hidden `
    -PassThru `
    -Environment @{"PORT"="$appPort"; "PYTHONUNBUFFERED"="1"}

if ($null -eq $serverProcess) {
    throw "❌ Error al iniciar el servidor Flask"
}

Write-Host "✅ Proceso Flask iniciado (PID: $($serverProcess.Id))" -ForegroundColor Green

# Esperar a que el servidor esté listo
Write-Step "Esperando a que el servidor esté listo (esto puede tomar 5-10 segundos)..."
$maxAttempts = 15
$attempt = 0
$serverReady = $false

while ($attempt -lt $maxAttempts) {
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:$appPort" -UseBasicParsing -ErrorAction SilentlyContinue
        if ($response.StatusCode -eq 200) {
            $serverReady = $true
            break
        }
    } catch {
        # Servidor aún no está listo
    }
    
    Start-Sleep -Seconds 1
    $attempt++
    Write-Host "  ⏳ Intento $attempt/$maxAttempts..." -ForegroundColor Gray
}

Write-Host ""
if ($serverReady) {
    Write-Host "✅ Servidor respondiendo correctamente (HTTP 200)" -ForegroundColor Green
    Write-Host ""
    Write-Step "Abriendo navegador..."
    Start-Process "http://localhost:$appPort"
    Write-Host ""
    Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Green
    Write-Host "✅ SISTEMA INICIADO EXITOSAMENTE" -ForegroundColor Green
    Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Green
    Write-Host ""
    Write-Host "📍 URL: http://localhost:$appPort" -ForegroundColor Cyan
    Write-Host "🔐 Credenciales: admin@airis.com / admin123" -ForegroundColor Cyan
    Write-Host "📊 Logs: $logsDir\agent-email.log" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "💡 Información:" -ForegroundColor Yellow
    Write-Host "   • El servidor está ejecutándose en background" -ForegroundColor Gray
    Write-Host "   • Los logs se guardan en: backend/logs/agent-email.log" -ForegroundColor Gray
    Write-Host "   • Para detener: Abre Task Manager y finaliza 'python.exe'" -ForegroundColor Gray
    Write-Host "   • O ejecuta: Stop-Process -Id $($serverProcess.Id)" -ForegroundColor Gray
    Write-Host ""
} else {
    Write-Host "⚠️  Timeout esperando que el servidor esté listo" -ForegroundColor Yellow
    Write-Host "    El servidor puede estar iniciándose. Revisa los logs." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "📊 Ubicación de logs: $logsDir" -ForegroundColor Cyan
    Write-Host ""
}

Write-Host "Presiona Enter para continuar o cierra esta ventana..." -ForegroundColor Yellow
Read-Host
