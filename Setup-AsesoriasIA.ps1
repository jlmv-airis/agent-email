# Configuración de Entorno - Agente de Email AI

$projectRoot = $PSScriptRoot
$n8nLocalDir = Join-Path $projectRoot "Code\n8n-local"
$n8nDataDir = Join-Path $n8nLocalDir "n8n_data"
$postgresDataDir = Join-Path $n8nLocalDir "postgres_data"

Write-Host "--- INICIANDO CONFIGURACIÓN DE ENTORNO ---" -ForegroundColor Cyan

# 1. Crear directorios de persistencia
Write-Host "Creando carpetas de datos locales..." -ForegroundColor Yellow
if (!(Test-Path $n8nDataDir)) { New-Item -ItemType Directory -Path $n8nDataDir }
if (!(Test-Path $postgresDataDir)) { New-Item -ItemType Directory -Path $postgresDataDir }

# 2. Verificar Docker
Write-Host "Verificando Docker..." -ForegroundColor Yellow
$dockerCheck = docker --version 2>$null
if ($dockerCheck) {
    Write-Host "Docker detectado: $dockerCheck" -ForegroundColor Green
} else {
    Write-Host "ADVERTENCIA: Docker no está instalado o no está en el PATH." -ForegroundColor Red
}

# 3. Verificar Docker Compose
$composeCheck = docker-compose --version 2>$null
if ($composeCheck) {
    Write-Host "Docker Compose detectado: $composeCheck" -ForegroundColor Green
} else {
    Write-Host "ADVERTENCIA: Docker Compose no está instalado." -ForegroundColor Red
}

# 4. Verificar Ngrok (Opcional)
Write-Host "Verificando Ngrok..." -ForegroundColor Yellow
$ngrokCheck = ngrok --version 2>$null
if ($ngrokCheck) {
    Write-Host "Ngrok detectado: $ngrokCheck" -ForegroundColor Green
} else {
    Write-Host "Ngrok: Descarga manual en https://ngrok.com/download" -ForegroundColor Gray
}

Write-Host "`n--- CONFIGURACIÓN FINALIZADA ---" -ForegroundColor Cyan
Write-Host "Para levantar el entorno ejecuta estos 3 pasos:" -ForegroundColor White
Write-Host "1. cd Code/n8n-local"
Write-Host "2. docker-compose up -d"
Write-Host "3. Inicializar base de datos:"
Write-Host "   docker exec -i n8n-local-postgres-1 psql -U n8n_user -d n8n_db -c '"
Write-Host "   CREATE TABLE IF NOT EXISTS usuarios (id SERIAL PRIMARY KEY, username VARCHAR(50) UNIQUE NOT NULL, nombre VARCHAR(100), email VARCHAR(255), password_hash VARCHAR(255), rol VARCHAR(20) DEFAULT '\''operador'\'', notas TEXT, activo BOOLEAN DEFAULT TRUE, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);"
Write-Host "   CREATE TABLE IF NOT EXISTS grupos (id SERIAL PRIMARY KEY, nombre VARCHAR(100), color VARCHAR(20), tipo VARCHAR(20));"
Write-Host "   CREATE TABLE IF NOT EXISTS configuracion (clave VARCHAR(50) PRIMARY KEY, valor VARCHAR(255));"
Write-Host "   CREATE TABLE IF NOT EXISTS mensajes_entrantes (id SERIAL PRIMARY KEY, fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP, remitente VARCHAR(255), asunto TEXT, mensaje TEXT, thread_id VARCHAR(100), cuenta_empresa VARCHAR(255), leido BOOLEAN DEFAULT FALSE, de_operador BOOLEAN DEFAULT FALSE, asignado_a VARCHAR(50));"
Write-Host "   INSERT INTO configuracion (clave, valor) VALUES ('\''caducidad_hilos_dias'\'', '\''7'\'') ON CONFLICT DO NOTHING;"
Write-Host "   '"
Write-Host "4. Instalar Python: pip install -r requirements.txt"
Write-Host "5. Iniciar servidor: python server.py"
