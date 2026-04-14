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
$venvDir = Join-Path $projectRoot ".venv"
$venvPython = Join-Path $venvDir "Scripts\python.exe"
$requirementsFile = Join-Path $projectRoot "requirements.txt"
$appPort = $Port

Write-Host "=========================================="
Write-Host "  AGENT EMAIL AIRIS V1 - INICIO LOCAL"
Write-Host "=========================================="
Write-Host "Puerto configurado: $appPort"

Assert-Command -CommandName "python"

Set-Location $projectRoot

if (-not (Test-Path $venvPython)) {
    Write-Step "Creando entorno virtual (.venv)"
    python -m venv .venv
}

if (-not (Test-Path $venvPython)) {
    throw "No se pudo crear el entorno virtual en '$venvDir'."
}

if (-not $SkipInstall) {
    Write-Step "Actualizando pip"
    & $venvPython -m pip install --upgrade pip

    if (Test-Path $requirementsFile) {
        Write-Step "Instalando dependencias de requirements.txt"
        & $venvPython -m pip install -r $requirementsFile
    } else {
        Write-Host "Aviso: no existe requirements.txt, se omite instalacion base." -ForegroundColor Yellow
    }

    Write-Step "Instalando dependencias requeridas por backend/server.py"
    & $venvPython -m pip install pyjwt cryptography imap-tools
} else {
    Write-Host "SkipInstall activo: se omite instalacion de paquetes." -ForegroundColor Yellow
}

if (-not (Test-Path $backendDir)) {
    throw "No se encontro la carpeta backend en '$projectRoot'."
}

$portOwner = Get-PortOwnerInfo -Port $appPort
if ($portOwner) {
    throw "El puerto $appPort ya esta en uso por PID $($portOwner.Pid) ($($portOwner.Name)). Deten ese proceso o cambia el puerto antes de iniciar."
}

Write-Step "Abriendo aplicacion en navegador"
Start-Process "http://localhost:$appPort"

Write-Step "Iniciando Flask en backend/server.py (Ctrl+C para detener)"
Set-Location $backendDir
$env:PORT = "$appPort"
& $venvPython "server.py"
