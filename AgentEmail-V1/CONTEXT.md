# 📋 CONTEXTO COMPLETO DEL PROYECTO

**Agent Email AIRIS** - Sistema SaaS de gestión de correos electrónicos

---

## 🎭 ROL DEL ASISTENTE AI

### Identidad
- **Nombre:** Asistente de Desarrollo (Agent AI)
- **Rol Principal:** Experto en desarrollo de software, especializado en Python, Flask, JavaScript, bases de datos SQLite, APIs REST, seguridad y automatización
- **Proyecto Actual:** Agent Email AIRIS V1.0.16

### Responsabilidades del Asistente
- ✅ Analizar y comprender el código del proyecto
- ✅ Sugerir mejoras y optimizaciones
- ✅ Crear y modificar archivos según requerimientos
- ✅ Ejecutar comandos de terminal y Git
- ✅ Mantener documentación actualizada
- ✅ Proponer mejoras de seguridad

### 🚫 Reglas No Negociables

1. **NUNCA** hacer merge con la rama `main` sin autorización explícita
2. **NUNCA** subir cambios a GitHub sin supervisión del usuario
3. **NUNCA** hacer commits por cambios menores (corrección de una letra = NO)
4. **NUNCA** ejecutar comandos destructivos sin confirmación previa
5. **SIEMPRE** actualizar la versión en el footer cuando se cambie de rama
6. **SIEMPRE** renombrar el archivo de plan cuando se cambie de rama (preservar historial)
7. **SIEMPRE** mantener actualizado el archivo de seguridad con nuevas recomendaciones

### 📊 Estado Actual

| Campo | Valor |
|-------|-------|
| Rama activa | `v1.0.16` |
| Versión | V1.0.16 |
| Plataforma actual | Windows |
| Ubicación del Proyecto | `AgentEmail-V1/` |
| Fecha de actualización | 27 de abril de 2026 |
| Tema | Solo oscuro (dark mode) |

---

## 🏗️ ARQUITECTURA DEL SISTEMA

### Stack Tecnológico
| Capa | Tecnología |
|------|------------|
| **Backend** | Python 3.11+, Flask, SQLite |
| **Frontend** | HTML5, TailwindCSS (CDN), JavaScript vanilla |
| **Base de datos** | SQLite con cifrado Fernet (AES) |
| **Email** | IMAP/SMTP con imap_tools |
| **Auth** | JWT tokens |
| **Seguridad** | Fernet encryption, headers CSP |

### Estructura de Archivos
```
AgentEmail-V1/
├── backend/
│   ├── server.py           # API principal (~1500 líneas)
│   ├── config.py          # Configuración centralizada
│   ├── security.py        # Headers + validadores
│   ├── health.py          # Health checks
│   ├── database.py        # Estadísticas BD
│   ├── backup_manager.py  # Sistema de backups
│   ├── init_db.py        # Migraciones
│   ├── logger_config.py   # Logging
│   ├── logs/              # Logs del servidor
│   └── agent_email.db     # SQLite
├── frontend/
│   ├── login.html         # Página de login
│   └── index.html         # Dashboard principal (~3100 líneas)
├── database/
│   └── agent_email.db     # Copia de seguridad BD
├── docs/                  # Documentación
│   ├── guias/
│   ├── fases/
│   ├── checklists/
│   ├── referencia/
│   └── plan/             # Planes por versión
├── scripts/               # Scripts de control
│   ├── INICIAR-SISTEMA.ps1
│   ├── DETENER-SISTEMA.ps1
│   └── DIAGNOSTICO.ps1
├── .env                  # Configuración (NO commitear)
├── .key                  # Llave Fernet (NO commitear)
└── requirements.txt       # Dependencias Python
```

---

## 🚀 CÓMO LEVANTAR EL PROYECTO

### 🖥️ Windows

#### Requisitos Previos
- Python 3.10+ instalado
- PowerShell 5.1+

#### Pasos
```powershell
# 1. Navegar al proyecto
cd "C:\Users\Jorge Meneses\Desktop\Proyectos AIRIS\Desarrollo\Proyecto_Agente Email\agent-email\AgentEmail-V1"

# 2. (Opcional) Crear entorno virtual
python -m venv ia_env

# 3. Activar entorno virtual
.\ia_env\Scripts\Activate.ps1

# 4. Instalar dependencias
pip install -r requirements.txt

# 5. Iniciar servidor
cd backend
python server.py
```

#### Con Scripts Automatizados
```powershell
# Opción recomendada
powershell -ExecutionPolicy Bypass -File INICIAR-SISTEMA.ps1
```

**URL de acceso:** http://localhost:8000

---

### 🍎 macOS / Linux

#### Requisitos Previos
- Python 3.10+
- Bash o Zsh

#### Pasos
```bash
# 1. Navegar al proyecto
cd ~/Proyectos/AgentEmail/AgentEmail-V1

# 2. (Opcional) Crear entorno virtual
python3 -m venv ia_env

# 3. Activar entorno virtual
source ia_env/bin/activate

# 4. Instalar dependencias
pip install -r requirements.txt

# 5. Iniciar servidor
cd backend
python server.py
```

#### Con Scripts Automatizados
```bash
# Opción recomendada
bash INICIAR-SISTEMA.sh
```

---

## 🔐 CREDITENCIAS

| Campo | Valor |
|-------|-------|
| Email admin | `admin@airis.com` |
| Contraseña | `admin` |

---

## 📊 ESTADO ACTUAL DEL PROYECTO

### ✅ Completado

| Módulo | Estado | Notas |
|--------|--------|-------|
| Login/JWT | ✅ Listo | Tokens con expiración |
| Dashboard Gmail-style | ✅ Listo | UI moderna dark |
| Sincronización IMAP | ✅ Listo | Multi-cuenta |
| Editor de respuesta | ✅ Listo | CC/CCO, adjuntos |
| Estados de tickets | ✅ Listo | PENDIENTE → ASIGNADO → RESPONDIDO → CERRADO |
| Sistema de etiquetas | ✅ Listo | CRUD completo |
| Borradores | ✅ Listo | Autoguardado |
| Backups | ✅ Listo | Auto y manual |
| Seguridad | ✅ Parcial | Headers + validación |
| IA (Gemini/Groq) | ✅ Listo | Cascada de modelos |

### ⚠️ Pendientes / En Progreso

| Tarea | Prioridad | Estado |
|-------|-----------|--------|
| Exportación PDF/Excel | Media | Pendiente |
| 2FA Authentication | Alta | Pendiente |
| Rate limiting producción | Alta | Pendiente |
| HTTPS en producción | Alta | Pendiente |

---

## 📝 ÚLTIMOS CAMBIOS REALIZADOS (v1.0.16)

### Cambios Realizados
- [x] Rama `v1.0.16` creada para implementación de 2FA, Rate Limiting, HTTPS, Reportes
- [x] Versión actualizada en footer a v1.0.16
- [x] Sincronización de documentación a v1.0.16
- [x] Creado v1.0.16-plan.md con objetivos e implementación técnica
- [x] Actualizado CONTEXT.md, README.md, AI-README.md, AGENTS.md

---

## 📋 REGLAS DE NOMENCLATURA

### Archivo de Plan por Versión
- **Ubicación:** `docs/plan/[VERSION]-plan.md`
- **Ejemplo:** `docs/plan/v1.0.13-plan.md`
- **Regla:** Al cambiar de rama, renombrar el archivo actual (preservar historial) y crear uno nuevo para la nueva versión

### Actualización de Versión
- Al cambiar de rama (ej: v1.0.13 → v1.0.14):
  1. Actualizar `frontend/index.html` línea ~641: `<span>v1.0.X</span>` → `<span>v1.0.Y</span>`
  2. Renombrar `docs/plan/v1.0.X-plan.md` → preservar
  3. Crear `docs/plan/v1.0.Y-plan.md` nuevo
  4. Actualizar este archivo (CONTEXT.md) con nueva rama

---

## 🛡️ SEGURIDAD

### Estado Actual
- ✅ Headers de seguridad configurados (CSP, X-Frame-Options, etc.)
- ✅ Validación de inputs
- ✅ Cifrado de credenciales IMAP con Fernet
- ⚠️ Rate limiting solo en desarrollo
- ⚠️ Puerto 0.0.0.0 expuesto

### Recomendaciones de Seguridad
1. Implementar 2FA
2. Configurar HTTPS con nginx
3. Usar variables de entorno del sistema (no .env en producción)
4. Habilitar rate limiting en producción
5. Cambiar HOST a 127.0.0.1

**Archivo de referencia:** `docs/referencia/seguridad-auditoria.md`

---

## 📞 CONTACTOS

| Rol | Nombre | Email |
|-----|--------|-------|
| Desarrollador | Jorge Meneses | jorge.meneses@airis-ae.com.mx |

---

## 🎨 MEJORAS UI IMPLEMENTADAS (v1.0.15-ui-test)

### Diseño
- Sistema de design tokens con CSS custom properties
- Botones modernos con gradientes y efectos hover
- Tarjetas con bordes gradiente y animaciones
- Notificaciones toast integradas (4 tipos)
- Login.html rediseñado con efectos visuales

### Responsive
- Menú móvil con overlay
- Inspector a pantalla completa en móvil
- Breakpoints: 1024px, 768px, 480px
- Sidebar colapsable en móvil

### Tema
- **Solo modo oscuro** (light mode eliminado por conflictos con Tailwind CDN)
- Clases de compatibilidad mantenidas

---

**Última actualización:** 27 de abril de 2026
**Versión:** V1.0.15
**Rama:** v1.0.15-ui-test
