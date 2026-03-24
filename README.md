# Agente de Email AI - Gestión Híbrida de Tickets

Este proyecto es un sistema de automatización para la gestión de correos electrónicos utilizando **n8n**, diseñado para operar de forma híbrida (automática y manual) mediante un panel de control interactivo.

## 🚀 Características Principales

- **Agente Maestro Multicuenta:** Capacidad para gestionar múltiples bandejas de entrada de forma centralizada.
- **IA Generativa:** Procesamiento de lenguaje natural para categorizar y responder correos.
- **Gestión Híbrida:** Sistema de asignación de tickets para intervención humana cuando la IA lo requiera.
- **Panel de Control:** Interfaz HTML/JS para la visualización de logs, mensajes y gestión de cuentas en tiempo real.
- **Entorno Local:** Configuración basada en Docker para despliegue rápido de n8n y PostgreSQL.

## 📂 Estructura del Proyecto

- `Code/`: Contiene los flujos de n8n en formato JSON listos para importar.
  - `agente-email.json`: Lógica principal del agente.
  - `api-*.json`: Endpoints para la comunicación con el panel frontal.
- `Code/n8n-local/`: Configuración de Docker Compose para el entorno de desarrollo.
- `Panel.html`: Interfaz de usuario para la administración del sistema.
- `Setup-AsesoriasIA.ps1`: Script de configuración inicial para el entorno local.

## 🛠️ Requisitos Previos

- Docker y Docker Compose.
- Node.js (opcional, para herramientas adicionales).
- Una cuenta de n8n (o usar la versión local incluida).

## 🔧 Instalación y Uso

1. **Configurar el entorno:**
   Ejecuta el script de configuración inicial:
   ```powershell
   ./Setup-AsesoriasIA.ps1
   ```

2. **Iniciar n8n local:**
   Navega a `Code/n8n-local/` y levanta los servicios:
   ```bash
   docker-compose up -d
   ```

3. **Acceder al Panel:**
   Abre `Abrir-Panel.bat` para iniciar la interfaz de gestión.

## 📝 Notas de Versión
- **V 0.0.1:** Estructura inicial, flujos base de n8n y panel de administración funcional.

---
Desarrollado para la optimización de soporte al cliente y gestión de comunicaciones empresariales.
