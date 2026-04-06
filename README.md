# Agente de Email AI - Consola de Administración Global (V 1.2)

Sistema de gestión híbrida masiva para correos electrónicos, diseñado para centralizar la operación de más de **150 empresas** en una interfaz profesional estilo Gmail, con asistencia de IA (Gemini) y lógica de hilos inteligentes.

## 🌟 Nuevas Funcionalidades (V 1.2)
- **Interfaz Gmail-Pro:** Panel administrativo optimizado con buscador de empresas y vista densa de mensajes.
- **Gestión de Hilos:** Agrupamiento automático de correos por `thread_id` para trazabilidad completa de conversaciones.
- **Regla de Caducidad Individual:** Selector global para definir el cierre de hilos por inactividad (3, 7 o 15 días).
- **Asignación Manual:** Capacidad para que el Administrador delegue hilos específicos a operadores.
- **Banner de Gestión Maestra:** Distintivo visual para perfiles de alto nivel con privilegios totales.

---

## 🚀 Guía de Despliegue Paso a Paso (Windows)

Sigue estos pasos para poner el proyecto en marcha en un entorno Windows:

### 1. Requisitos Previos
- **Docker Desktop:** [Descárgalo aquí](https://www.docker.com/products/docker-desktop/) e instálalo. Asegúrate de que esté iniciado.
- **Python 3.x:** Para servir el panel de control localmente.
- **Git:** Para clonar y gestionar el repositorio.

### 2. Clonación y Configuración de Carpetas
Abre una terminal de PowerShell como administrador y ejecuta:
```powershell
# Clonar el proyecto (si no lo has hecho)
git clone <url-del-repositorio>
cd agent-email

# Ejecutar script de preparación de volúmenes Docker
.\Setup-AsesoriasIA.ps1
```

### 3. Levantar la Infraestructura (Docker)
Levanta n8n y la base de datos PostgreSQL:
```powershell
cd Code/n8n-local
docker-compose up -d
```
*n8n estará activo en: http://localhost:5678*

### 4. Inicialización de la Base de Datos
Ejecuta este comando para crear las tablas necesarias para la V 1.2:
```powershell
docker exec -i n8n-local-postgres-1 psql -U n8n_user -d n8n_db -c "
CREATE TABLE IF NOT EXISTS usuarios (id SERIAL PRIMARY KEY, username VARCHAR(50) UNIQUE, password_hash VARCHAR(255), rol VARCHAR(20));
CREATE TABLE IF NOT EXISTS grupos (id SERIAL PRIMARY KEY, nombre VARCHAR(100), color VARCHAR(20), tipo VARCHAR(20));
CREATE TABLE IF NOT EXISTS configuracion (clave VARCHAR(50) PRIMARY KEY, valor VARCHAR(255));
CREATE TABLE IF NOT EXISTS mensajes_entrantes (id SERIAL PRIMARY KEY, fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP, remitente VARCHAR(255), asunto TEXT, mensaje TEXT, thread_id VARCHAR(100), cuenta_empresa VARCHAR(255), leido BOOLEAN DEFAULT FALSE, de_operador BOOLEAN DEFAULT FALSE, asignado_a VARCHAR(50));
INSERT INTO usuarios (username, password_hash, rol) VALUES ('admin', 'admin', 'admin') ON CONFLICT DO NOTHING;
INSERT INTO configuracion (clave, valor) VALUES ('caducidad_hilos_dias', '7') ON CONFLICT DO NOTHING;
"
```

### 5. Ejecutar el Panel de Control
Vuelve a la raíz del proyecto e inicia el servidor web:
```powershell
python server.py
```
**Acceso al Panel:** Abre tu navegador en [http://localhost:8000/Panel.html](http://localhost:8000/Panel.html).

---

## 📂 Estructura del Proyecto
- **/Code:** Contiene los flujos JSON de n8n y la configuración de Docker Compose.
- **/Mockup:** Diseños e infografías del proceso de desarrollo.
- **Panel.html:** Interfaz principal de administración (V 1.2 Forzada).
- **server.py:** Servidor ligero para desarrollo local.

---
**Desarrollado por:** AIRIS AI Team  
**Estado:** Estable (Rama de Desarrollo)
