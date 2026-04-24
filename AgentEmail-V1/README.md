# 📧 Agent Email AIRIS - Versión V1.0.16

Este es el sistema SaaS unificado de gestión de correos electrónicos. Se ha refactorizado para eliminar dependencias externas (como n8n) y utilizar una arquitectura limpia de **Python (Flask) + SQLite**.

## 📌 Estado Actual del Proyecto
- **Versión:** V1.0.16
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

## ✨ Características Implementadas (V1.0.16)

### 🖥️ Interfaz de Usuario
- [x] **Dashboard Estilo Gmail:** Panel de correos con diseño moderno similar a Gmail
- [x] **Inspector de Correos:** Vista detallada del correo con estilo Gmail (De, Para, Fecha)
- [x] **Gestión de Cc y Cco (BCC):** Modal de respuesta con campos editables y soporte multi-destinatario.
- [x] **Sidebar con Empresas:** Navegación por buzones de empresas
- [x] **Gráficos de Tendencias:** Estadísticas visuales de tickets
- [x] **Gestión de Adjuntos:** Barra visual de archivos adjuntos con eliminación individual y previsualización.
- [x] **UI de Operador Simplificada:** Interfaz limpia que oculta controles de gestión para operadores.
- [x] **Mensajes de Confirmación:** Al enviar, responder o borrar correos se muestra resultado detallado.

### 📧 Gestión de Correos
- [x] **Sincronización IMAP:** Sincronización transparente de correos de múltiples cuentas
- [x] **Copia Automática en Enviados:** Al enviar, se guarda copia en carpeta Enviados del servidor webmail
- [x] **Entregabilidad Optimizada (SMTP):** Cabeceras profesionales (`Message-ID`, `Date`, `Reply-To`)
- [x] **Soporte Multi-correo:** Envío a múltiples destinatarios separados por comas.
- [x] **Estados Automáticos:** Pendiente → Asignado → Respondido → Cerrado
- [x] **Bandeja de Borradores:** Autoguardado silencioso del editor
- [x] **Papelera Local y Webmail:** Al borrar se mueve a Trash en ambos sistemas
- [x] **Control de Errores:** Mensaje detallado si el destinatario no existe o buzón lleno

### 🤖 Inteligencia Artificial (Engine 3.1)
- [x] **Cascada Inteligente de IA:** Soporte dinámico para **Gemini 3.1 Pro**, **Gemini 2.5 Flash** y **Gemini 1.5 Flash**.
- [x] **Identificación de Modelos por Llave:** Soporte para llaves `AQ.` y `AIzaSy` con detección automática.

### ⚙️ Administración
- [x] **Gestión de Colaboradores:** Crear/editar/eliminar operadores
- [x] **Gestión de Empresas:** Agregar cuentas de correo IMAP
- [x] **Cifrado AES de Credenciales:** Seguridad mediante llave `.key` local.
- [x] **Actualización de Contadores:** Se actualizan automáticamente después de acciones en masivo

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

**Última actualización:** viernes, 24 de abril de 2026
**Versión:** V1.0.16
**Objetivo:** Mantener el código en `index.html` como la única fuente de verdad para el panel administrativo.