# 📧 Agent Email AIRIS V1.1.21

Sistema SaaS de gestión de correos electrónicos estilo Gmail con inteligencia artificial integrada. Arquitectura **Python (Flask) + SQLite + JavaScript vanilla**.

## 📌 Estado Actual

- **Versión:** V1.1.21
- **Acceso:** [http://localhost:8000](http://localhost:8000)
- **Credenciales:** `admin@airis.com` / `admin123`

## 🚀 Inicio Rápido

```powershell
# Windows (PowerShell)
powershell -ExecutionPolicy Bypass -File .\INICIAR-SISTEMA.ps1

# Manual
cd AgentEmail-V1
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python backend\server.py
```

```bash
# macOS / Linux
source .venv/bin/activate
pip install -r requirements.txt
python backend/server.py
```

## ✨ Características

### 🖥️ Dashboard
- [x] Interfaz estilo Gmail con modo oscuro
- [x] Inspector de correos con vista detallada
- [x] Sidebar multi-empresa con carpetas (Entrada, Enviados, Borradores, Programados, Papelera, Spam)
- [x] Contadores por carpeta en tiempo real
- [x] Editor de respuesta con CC/CCO y formato de texto
- [x] Bandeja de borradores con autoguardado (2s)
- [x] Gráficos de analytics por operador y empresa
- [x] Búsqueda global con debounce
- [x] Gestión de adjuntos con previsualización

### 📧 Correos Programados (Nuevo en v1.1.21)
- [x] **Programar envío:** Botón "Programar" junto a "Enviar" con selector de fecha/hora
- [x] **Carpeta Programados:** Visualización en sidebar con contador
- [x] **Cancelar:** Soft-delete con confirmación
- [x] **Editar:** Modificar contenido, destinatario, CC, fecha antes del envío
- [x] **Envío automático:** APScheduler con polling cada 30s
- [x] **Modal de listado:** Todos los programados en un solo vistazo

### 📬 Gestión de Correos
- [x] Sincronización IMAP multi-cuenta
- [x] Envío SMTP con SSL/STARTTLS
- [x] Copia en carpeta Enviados del servidor (Sent Mail)
- [x] Cabeceras profesionales (Message-ID, Date, Reply-To, In-Reply-To)
- [x] Estados de tickets: Pendiente → Asignado → Respondido → Cerrado
- [x] Papelera local y remota (IMAP Trash)

### 🤖 Inteligencia Artificial
- [x] Cascada de modelos Gemini (Pro, Flash, 1.5 Flash)
- [x] Detección automática de API Key (prefijo `AQ.` o `AIzaSy`)
- [x] Autocompletar respuestas desde el editor

### ⚙️ Administración
- [x] CRUD de operadores y empresas
- [x] Cifrado Fernet (AES) de credenciales IMAP
- [x] Backups automáticos y manuales con retención
- [x] Seguridad: JWT, CSP headers, rate limiting, validación de inputs

## 🔧 Configuración IA

1. Obtén API Key en https://aistudio.google.com/app/apikey
2. Ve a ⚙️ Configuración → Sección IA
3. Ingresa la API Key y guarda

## 📊 Estados de Tickets

| Estado | Descripción |
|--------|-------------|
| ⏳ Pendiente | Correo nuevo, sin asignar |
| 🔄 Asignado | Asignado a un operador |
| ✅ Respondido | Operador ha respondido |
| 🔒 Cerrado | Ticket completado |

## 🛠️ Stack Tecnológico

| Capa | Tecnología |
|------|------------|
| Backend | Python 3.11+, Flask, SQLite, APScheduler |
| Frontend | HTML5, TailwindCSS (CDN), JavaScript vanilla, Chart.js |
| Seguridad | JWT, Fernet (AES), CSP Headers |
| Email | IMAP (imap_tools), SMTP (smtplib) |
| IA | Google Gemini API |

## 📁 Estructura

```
AgentEmail-V1/
├── backend/
│   ├── server.py          # API Flask (~2100 líneas)
│   ├── config.py          # Configuración centralizada
│   ├── security.py        # Headers + validación
│   ├── init_db.py         # Migraciones BD
│   ├── database.py        # Optimización índices
│   ├── backup_manager.py  # Backups
│   └── logs/              # Logs del servidor
├── frontend/
│   ├── index.html         # Dashboard (~5000 líneas)
│   └── login.html         # Página de login
├── docs/plan/             # Historial de planes
├── scripts/               # PowerShell, CMD, Bash
└── requirements.txt
```

---

**Última actualización:** 18 de mayo de 2026
**Versión:** V1.1.21