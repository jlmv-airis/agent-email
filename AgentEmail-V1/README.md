# 📧 Agent Email AIRIS - Versión V1.0.10

Este es el sistema SaaS unificado de gestión de correos electrónicos. Se ha refactorizado para eliminar dependencias externas (como n8n) y utilizar una arquitectura limpia de **Python (Flask) + SQLite**.

## 📌 Estado Actual del Proyecto
- **Versión:** V1.0.10
- **Acceso:** [http://localhost:8000](http://localhost:8000) (Se requiere login).
- **Flujo:** Login ➔ Redirección a Dashboard (index.html).

## 📁 Estructura de Archivos
- `/backend`: Servidor Flask (`server.py`) y llave de cifrado (`.key`).
- `/frontend`: Interfaz de usuario (`login.html` e `index.html`).
- `/database`: Base de datos local SQLite (`agent_email.db`).
- `/logs`: Archivos de log del sistema.

## 🔐 Credenciales por Defecto
- **Email:** `admin@airis.com`
- **Contraseña:** `admin`

## 🚀 Cómo Iniciar el Sistema

### Opción 1: Script de PowerShell (Recomendado)
```powershell
.\INICIAR-SISTEMA.ps1
```

### Opción 2: Manual
```bash
cd backend
python server.py
```
Luego accede a: http://localhost:8000

## ✨ Características Implementadas (V1.0.10)

### 🖥️ Interfaz de Usuario
- [x] **Dashboard Estilo Gmail:** Panel de correos con diseño moderno similar a Gmail
- [x] **Inspector de Correos:** Vista detallada del correo con estilo Gmail (De, Para, CC, Fecha)
- [x] **Sidebar con Empresas:** Navegación por buzones de empresas
- [x] **Gráficos de Tendencias:** Estadísticas visuales de tickets
- [x] **Filtros de Búsqueda:** Filtrado por estado, fecha, empresa

### 📧 Gestión de Correos
- [x] **Sincronización IMAP:** Sincronización transparente de correos de múltiples cuentas
- [x] **Envío Real SMTP:** Integración nativa para respuestas reales con credenciales mapeadas.
- [x] **Estados Automáticos Dinámicos:** Pendiente → Asignado → Respondido por [Operador] → Cerrado
- [x] **Bandeja de Borradores Avanzada:** Autoguardado silencioso del editor y ventana "Mis Borradores" dedicada.
- [x] **Responder/Reenviar Estilo Gmail:** Modal rediseñado, barra superior enriquecida (Emojis, Color, Links, Attachments visuales) y citas históricas adjuntas.

### 🤖 Inteligencia Artificial
- [x] **Generación de Respuestas con IA:** Integración con Google Gemini
- [x] **Configuración de API Key:** Panel de admin para configurar Gemini
- [x] **Verificación de Cuota:** Muestra estado de la API (funcionando/agotada)

### ⚙️ Administración
- [x] **Gestión de Colaboradores:** Crear/editar/eliminar operadores
- [x] **Gestión de Empresas:** Agregar cuentas de correo IMAP
- [x] **Sincronización Manual:** Forzar descarga de correos
- [x] **Base de Datos Local:** SQLite con cifrado Fernet

### 🎨 Mejoras Visuales Recientes
- [x] Botón Eliminar con estilo Gmail (solo icono)
- [x] Línea divisoria entre header y cuerpo del mensaje
- [x] "PARA:" en negrita color oscuro
- [x] Botón de eliminar en barra de acciones inferiores

## 🔧 Configuración de API de IA

Para habilitar la generación automática de respuestas:

1. Obtén una API Key de **Google Gemini** en: https://aistudio.google.com/app/apikey
2. Abre **⚙️ Configuración** en el panel
3. En la sección "Configuración IA", ingresa tu API Key
4. Guarda y verifica que el estado muestre "API Key funcionando"

## 📊 Estados de Tickets

| Estado | Descripción |
|--------|-------------|
| ⏳ Pendiente | Correo nuevo, sin asignar |
| 🔄 En Proceso | Asignado a un operador |
| ✅ Respondido | Operator ha respondido |
| 🔒 Cerrado | Ticket completado |

## 🛠️ Tecnologías Usadas

- **Backend:** Python, Flask, SQLite
- **Frontend:** HTML, TailwindCSS, JavaScript
- **Seguridad:** JWT, Fernet Encryption
- **Email:** IMAP/SMTP

---

**Última actualización:** jueves, 16 de abril de 2026
**Objetivo:** Mantener el código en `index.html` como la única fuente de verdad para el panel administrativo.