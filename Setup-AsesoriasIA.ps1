# Setup-AsesoriasIA.ps1
# Script de configuración de entorno DevOps para Asesorías IA - Agent Email

Write-Host "--- Iniciando Configuración de Env: Asesorías IA ---" -ForegroundColor Cyan

# 1. Verificación de WSL2
Write-Host "`n[1/5] Verificando WSL2..." -ForegroundColor Yellow
$wslStatus = wsl --status 2>$null
if ($null -eq $wslStatus) {
    Write-Host "WSL no detectado o no habilitado." -ForegroundColor Red
    Write-Host "EJECUTA ESTE COMANDO EN UNA TERMINAL COMO ADMIN: wsl --install" -ForegroundColor Cyan
} else {
    Write-Host "WSL2 detectado correctamente." -ForegroundColor Green
}

# 2. Docker Desktop
Write-Host "`n[2/5] Verificando Docker Desktop..." -ForegroundColor Yellow
if (Get-Command docker -ErrorAction SilentlyContinue) {
    Write-Host "Docker está instalado." -ForegroundColor Green
} else {
    Write-Host "Docker no detectado. Descarga desde: https://desktop.docker.com/win/main/amd64/Docker%20Desktop%20Installer.exe" -ForegroundColor Cyan
}

# 3. Configuración de Memoria (.wslconfig)
Write-Host "`n[3/5] Configurando límites de memoria (8GB)..." -ForegroundColor Yellow
$wslPath = [System.IO.Path]::Combine($env:USERPROFILE, ".wslconfig")
$wslText = "[wsl2]`nmemory=8GB`nprocessors=4"

if (-not (Test-Path $wslPath)) {
    $wslText | Out-File -FilePath $wslPath -Encoding ascii -Force
    Write-Host "Archivo .wslconfig creado en $wslPath." -ForegroundColor Green
} else {
    Write-Host "El archivo .wslconfig ya existe." -ForegroundColor Gray
}

# 4. Despliegue de n8n con PostgreSQL
Write-Host "`n[4/5] Verificando infraestructura n8n..." -ForegroundColor Yellow
$projectDir = "Code/n8n-local"
if (Test-Path "$projectDir/docker-compose.yml") {
    Write-Host "Archivo docker-compose.yml listo en $projectDir" -ForegroundColor Green
} else {
    Write-Host "ERROR: No se encontró docker-compose.yml" -ForegroundColor Red
}

# 5. Túnel Ngrok
Write-Host "`n[5/5] Configuración de Túnel (Ngrok)..." -ForegroundColor Yellow
if (Get-Command choco -ErrorAction SilentlyContinue) {
    Write-Host "Instalando/Actualizando Ngrok vía Chocolatey..." -ForegroundColor Gray
    choco upgrade ngrok -y
} else {
    Write-Host "Ngrok: Descarga manual en https://ngrok.com/download" -ForegroundColor Gray
}

Write-Host "`n--- CONFIGURACIÓN FINALIZADA ---" -ForegroundColor Cyan
Write-Host "Para levantar el entorno ejecuta estos 3 pasos:" -ForegroundColor White
Write-Host "1. cd Code/n8n-local"
Write-Host "2. docker-compose up -d"
Write-Host "3. ngrok http 5678"
