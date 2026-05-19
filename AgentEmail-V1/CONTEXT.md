# 📋 CONTEXT.md - Agent Email AIRIS V1.0.15

**ÚNICO ARCHIVO DE CONTEXTO PARA LA IA**

---

## 🤖 Identidad del Asistente AI

**Nombre:** Agent AI (Asistente de Desarrollo AIRIS)
**Rol:** Experto en desarrollo de software full-stack
**Especialidades:**
- Python, Flask, SQLAlchemy
- JavaScript, HTML5, TailwindCSS
- Bases de datos SQLite
- APIs RESTful, JWT, cifrado AES
- IMAP/SMTP, DevOps, automatización

---

## 🎯 Objetivo del Proyecto

**Proyecto:** Agent Email AIRIS V1.0.15
**Descripción:** Sistema SaaS de gestión de correos electrónicos estilo Gmail
**Stack:** Python (Flask) + SQLite + JavaScript + TailwindCSS (CDN)

---

## 🚫 Reglas No Negociables

1. **NUNCA** hacer merge con `main` sin autorización
2. **NUNCA** subir cambios a GitHub sin supervisión
3. **NUNCA** hacer commits por cambios menores
4. **NUNCA** ejecutar comandos destructivos sin confirmación
5. **SIEMPRE** leer CONTEXT.md al inicio de cada conversación
6. **SIEMPRE** actualizar versión en footer al cambiar rama
7. **SIEMPRE** preservar historial de planes en `docs/plan/`
8. **SIEMPRE** mantener `docs/referencia/seguridad-auditoria.md` actualizado

---

## 📁 Estructura del Proyecto

```
AgentEmail-V1/
├── CONTEXT.md                    # ← LEER SIEMPRE
├── AGENTS.md                     # Reglas del asistente
├── docs/
│   ├── plan/
│   │   ├── v1.1.20-plan.md     # Historial
│   │   ├── v1.1.21-plan.md     # Historial
│   │   └── v1.1.22-plan.md     # Plan actual
│   └── referencia/
│       └── seguridad-auditoria.md
├── backend/
│   ├── server.py                # API principal (~1500 líneas)
│   ├── config.py                # Configuración centralizada
│   ├── security.py              # Headers + validadores
│   ├── health.py                # Health checks
│   ├── database.py              # Estadísticas BD
│   ├── backup_manager.py        # Sistema de backups
│   ├── init_db.py              # Migraciones
│   ├── logger_config.py         # Logging
│   ├── logs/                    # Logs del servidor
│   └── agent_email.db           # SQLite
├── frontend/
│   ├── login.html               # Página de login
│   └── index.html               # Dashboard (~3100 líneas)
├── scripts/
│   ├── INICIAR-SISTEMA.ps1
│   ├── DETENER-SISTEMA.ps1
│   └── DIAGNOSTICO.ps1
├── ia_env/                      # Entorno virtual Python
├── .env                         # Configuración (NO commitear)
├── .key                         # Llave Fernet (NO commitear)
└── requirements.txt              # Dependencias Python
```

---

## 🚀 CÓMO INICIAR EL PROYECTO (PASO A PASO)

### Requisitos Previos
- Python 3.10+ instalado
- PowerShell 5.1+ (Windows) o Bash (macOS/Linux)

### Windows
```powershell
# 1. Navegar al proyecto
cd "C:\Users\Jorge Meneses\Desktop\Proyectos AIRIS\Desarrollo\Proyecto_Agente Email\agent-email\AgentEmail-V1"

# 2. Activar entorno virtual
.\ia_env\Scripts\Activate.ps1

# 3. Instalar dependencias (solo primera vez)
pip install -r requirements.txt

# 4. Iniciar servidor
python backend\server.py
```

### macOS / Linux
```bash
cd AgentEmail-V1
source ia_env/bin/activate
pip install -r requirements.txt
python backend/server.py
```

### Con Scripts Automatizados (Windows)
```powershell
powershell -ExecutionPolicy Bypass -File scripts/INICIAR-SISTEMA.ps1
```

**URL de acceso:** http://localhost:8000
**Credenciales:**
- Email: `admin@airis.com`
- Contraseña: `admin`

---

## 🏗️ Arquitectura del Sistema

| Capa | Tecnología |
|------|------------|
| Backend | Python 3.11+, Flask, SQLite |
| Frontend | HTML5, TailwindCSS (CDN), JavaScript vanilla |
| Base de datos | SQLite con cifrado Fernet (AES) |
| Email | IMAP/SMTP con imap_tools |
| Auth | JWT tokens |
| Seguridad | Fernet encryption, headers CSP |
| IA | Gemini API, Groq (cascada de modelos) |

---

## ✅ Estado Actual del Proyecto

### Completado
- [x] Login/JWT con tokens
- [x] Dashboard Gmail-style (dark mode)
- [x] Sincronización IMAP multi-cuenta
- [x] Editor de respuesta con CC/CCO
- [x] Estados de tickets (Pendiente → Asignado → Respondido → Cerrado)
- [x] Sistema de etiquetas CRUD
- [x] Borradores con autoguardado
- [x] Backups automáticos y manuales
- [x] Seguridad (headers + validación)
- [x] IA con cascada de modelos

### Pendientes
- [ ] Exportación PDF/Excel
- [ ] 2FA Authentication
- [ ] Rate limiting en producción
- [ ] HTTPS en producción

---

## 📊 Estados de Tickets

| Estado | Descripción |
|--------|-------------|
| ⏳ Pendiente | Correo nuevo, sin asignar |
| 🔄 Asignado | Asignado a un operador |
| ✅ Respondido | Operador ha respondido |
| 🔒 Cerrado | Ticket completado |

---

## 🛠️ Tecnologías Usadas

| Categoría | Tecnología |
|-----------|------------|
| Backend | Python, Flask, SQLite |
| Frontend | HTML5, TailwindCSS, JavaScript |
| Seguridad | JWT, Fernet (AES) |
| Email | IMAP/SMTP (imap_tools) |
| IA | Gemini API, Groq |

---

## 🛡️ Seguridad

### Estado Actual
- ✅ Headers de seguridad (CSP, X-Frame-Options)
- ✅ Validación de inputs
- ✅ Cifrado de credenciales IMAP con Fernet
- ⚠️ Rate limiting solo en desarrollo
- ⚠️ Puerto 0.0.0.0 expuesto

### Recomendaciones
1. Implementar 2FA
2. Configurar HTTPS con nginx
3. Usar variables de entorno del sistema en producción
4. Habilitar rate limiting en producción
5. Cambiar HOST a 127.0.0.1

**Archivo de referencia:** `docs/referencia/seguridad-auditoria.md`

---

## 📋 Reglas de Nomenclatura

### Cambio de Rama (ej: v1.0.15 → v1.0.16)
1. Renombrar `docs/plan/v1.0.15-plan.md` → preservar historial
2. Crear `docs/plan/v1.0.16-plan.md` nuevo
3. Actualizar `frontend/index.html` footer (línea ~641)
4. Actualizar este archivo (CONTEXT.md) con nueva rama

---

## 📞 Contacto

| Rol | Nombre | Email |
|-----|--------|-------|
| Desarrollador | Jorge Meneses | jorge.meneses@airis-ae.com.mx |

---

**Última actualización:** 19 de mayo de 2026  
**Versión:** V1.1.24  
**Rama activa:** v1.1.24  
**Tema:** Toggle claro/oscuro (dark/light mode)

### Registro de Versiones (Historial Reciente)
- **v1.1.24**: Nueva rama baseline desde main post-merge. ✅
  - Cambios: Baseline con todas las mejoras de v1.1.23.
  - Estado: Estable.
- **v1.1.23**: Agregadas 10 cuentas IMAP, menú contextual, orden alfabético, toggle tema claro/oscuro. ✅
  - Cambios: 10 cuentas (RoldanMaquinaria, LipusMexico, SuministrosRiu, BerbelTextil, EdcomStore, Humber, MortonTool, SentruSystems, Limmanhur, RenovartE), right-click context menu (ctxMarkRead, ctxAssign, ctxDelete), orden alfabético en sidebar, toggle tema claro/oscuro, UI refinements (glass morphism, spark-bg/spark-border).
  - Estado: Estable.
- **v1.1.22**: Agregadas 8 nuevas cuentas IMAP y ocultado scrollbar del sidebar. ✅
  - Cambios: Nuevas cuentas (PushLine, Iron Inmobiliaria, Edificadora Peralta, Publicidad Rocha, Vintte, CIO Publicidad, Eventos FT, Inbox MD), scrollbar oculto en sidebar.
  - Estado: Estable.
- **v1.1.21**: Implementación de programación de correos (Send Later) estilo Gmail con APScheduler. ✅
  - Cambios: Nuevos endpoints CRUD para programados, scheduler automático, UI con carpeta y modales.
  - Estado: Estable.
- **v1.1.20**: Implementación de analítica por operador (Enviados vs Recibidos) en el dashboard. ✅
  - Cambios: Gráfico de barras, nuevo endpoint de API, registro de operador en envíos.
  - Estado: Estable.
