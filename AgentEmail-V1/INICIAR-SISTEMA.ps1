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

    Write-Step "Instalando dependencias desde requirements.txt"
    if (Test-Path $requirementsFile) {
        & $venvPython -m pip install -r $requirementsFile --quiet
    }
    
    Write-Step "Instalando paquetes adicionales"
    & $venvPython -m pip install requests python-json-logger flask-limiter pytest pytest-cov --quiet
}

if (-not (Test-Path $backendDir)) {
    throw "No se encontro la carpeta backend."
}

$portOwner = Get-PortOwnerInfo -Port $appPort
if ($portOwner) {
    Write-Host "Aviso: El puerto $appPort ya esta en uso" -ForegroundColor Yellow
    Write-Host "PID: $($portOwner.Pid) | Proceso: $($portOwner.Name)"
    throw "Libera el puerto o elige otro."
}

# Configurar variables de entorno para el proceso hijo
$env:PORT = "$appPort"
$env:PYTHONUNBUFFERED = "1"

Write-Step "Iniciando servicios..."

$serverProcess = Start-Process -FilePath $venvPython `
    -ArgumentList "server.py" `
    -WorkingDirectory $backendDir `
    -WindowStyle Hidden `
    -PassThru

if ($null -eq $serverProcess) {
    throw "Error al iniciar el servidor Flask"
}

Write-Host "Proceso Flask iniciado (PID: $($serverProcess.Id))" -ForegroundColor Green

Write-Step "Esperando a que el servidor este listo..."
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
    } catch { }
    
    Start-Sleep -Seconds 1
    $attempt++
}

if ($serverReady) {
    Write-Host "SISTEMA INICIADO EXITOSAMENTE" -ForegroundColor Green
    Write-Host "URL: http://localhost:$appPort" -ForegroundColor Cyan
    Start-Process "http://localhost:$appPort"
} else {
    Write-Host "Timeout esperando el servidor" -ForegroundColor Yellow
}
