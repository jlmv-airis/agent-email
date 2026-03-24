# Agente de Email AI - Gestión Híbrida de Tickets

Este proyecto es un sistema de automatización para la gestión de correos electrónicos utilizando **n8n**, diseñado para operar de forma híbrida (automática y manual) mediante un panel de control interactivo.

## 🚀 Guía de Inicio desde Cero

Sigue estos pasos para levantar el entorno completo en tu máquina local:

### 1. Requisitos Previos
- **Docker Desktop** instalado y en ejecución.
- **n8n** (incluido en el contenedor Docker del proyecto).
- Una **API Key de Google Gemini** (Obtenla en [Google AI Studio](https://aistudio.google.com/)).

### 2. Configuración Inicial
Ejecuta el script de PowerShell en la raíz del proyecto para crear las carpetas de persistencia de datos:
```powershell
.\Setup-AsesoriasIA.ps1
```

### 3. Levantar Infraestructura (Docker)
Navega a la carpeta de configuración y levanta los servicios de n8n y PostgreSQL:
```powershell
cd Code/n8n-local
docker-compose up -d
```
*Nota: n8n estará disponible en [http://localhost:5678](http://localhost:5678)*.

### 4. Configuración de Base de Datos
Crea las tablas necesarias ejecutando el siguiente comando en tu terminal (esto inyectará el SQL directamente en el contenedor):
```powershell
docker exec -i n8n-local-postgres-1 psql -U n8n_user -d n8n_db -c "CREATE TABLE IF NOT EXISTS cuentas_email (id SERIAL PRIMARY KEY, email VARCHAR(255) UNIQUE NOT NULL, activo BOOLEAN DEFAULT TRUE); CREATE TABLE IF NOT EXISTS mensajes_entrantes (id SERIAL PRIMARY KEY, fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP, remitente VARCHAR(255), asunto TEXT, mensaje TEXT, estatus VARCHAR(50) DEFAULT 'pendiente'); CREATE TABLE IF NOT EXISTS trazabilidad_logs (id SERIAL PRIMARY KEY, fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP, cuenta_email VARCHAR(255), asunto TEXT, estatus VARCHAR(50), respuesta_ia TEXT);"
```

### 5. Importación de Workflows en n8n
Importa los archivos JSON de la carpeta `Code/` en n8n:
1. **Agente Maestro (`agente-maestro-multicuenta.json`):** El motor principal que consulta la base de datos y llama a Gemini.
2. **API Listar Mensajes (`api-listar-mensajes.json`):** Alimenta la bandeja de entrada del Panel HTML.
3. **API Obtener Logs (`api-obtener-logs.json`):** Recupera las sugerencias de la IA para mostrarlas en el Panel.

---

## 📂 Explicación de los Workflows

### 🤖 Agente Maestro (IA Gemini)
- **Función:** Se ejecuta periódicamente para procesar cuentas activas.
- **Lógica:** Realiza una llamada directa (HTTP Request) a la API de **Gemini 2.0 Flash** enviando el contexto del ticket. 
- **Resultado:** Guarda la respuesta profesional generada en la tabla `trazabilidad_logs`.

### 📥 API Listar Mensajes
- **Función:** Actúa como un puente entre la base de datos y la interfaz visual.
- **Lógica:** Recibe una petición GET desde el Panel y devuelve los últimos 10 mensajes de la tabla `mensajes_entrantes`.

### 📋 API Obtener Logs
- **Función:** Proporciona la "inteligencia" al panel en tiempo real.
- **Lógica:** Cuando el usuario hace clic en un mensaje, esta API busca la última sugerencia de la IA para ese caso y la devuelve en formato JSON.

---

## 🔧 Uso del Panel de Control
1. Ejecuta `Abrir-Panel.bat` en la raíz del proyecto.
2. Asegúrate de que la URL en el panel sea `http://localhost:5678`.
3. Navega a **Bandeja de Entrada** para ver y gestionar los tickets asistidos por IA.

---
**Versión actual:** V 0.0.1 (Rama de Desarrollo)
