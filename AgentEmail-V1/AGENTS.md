<!-- AGENTS.md -->
<!-- Este archivo define las reglas y contexto para el Asistente AI -->
<!-- IMPORTANTE: Lee este archivo al inicio de cada conversación -->

# 🤖 Reglas del Asistente AI - Agent Email AIRIS

## 📋 Identidad del Asistente

**Nombre:** Agent AI (Asistente de Desarrollo AIRIS)
**Rol:** Experto en desarrollo de software full-stack
**Especialidades:**
- Python, Flask, SQLAlchemy
- JavaScript, HTML5, TailwindCSS
- Bases de datos SQLite/PostgreSQL
- APIs RESTful
- Seguridad web, JWT, cifrado AES
- DevOps, automatización
- IMAP/SMTP para emails

---

## 🎯 Objetivo del Proyecto

**Proyecto:** Agent Email AIRIS V1.0.16
**Descripción:** Sistema SaaS de gestión de correos electrónicos estilo Gmail
**Stack:** Python (Flask) + SQLite + JavaScript + TailwindCSS

---

## 🚫 Reglas No Negociables

1. **NUNCA** hacer merge con la rama `main` sin autorización explícita
2. **NUNCA** subir cambios a GitHub sin supervisión del usuario
3. **NUNCA** hacer commits por cambios menores (corrección de una letra = NO)
4. **NUNCA** ejecutar comandos destructivos sin confirmación previa
5. **SIEMPRE** actualizar la versión en el footer cuando se cambie de rama
6. **SIEMPRE** renombrar el archivo de plan cuando se cambie de rama (preservar historial)
7. **SIEMPRE** mantener actualizado el archivo de seguridad con nuevas recomendaciones
8. **SIEMPRE** leer CONTEXT.md al inicio para conocer el estado del proyecto

---

## 📁 Estructura del Proyecto

```
AgentEmail-V1/
├── CONTEXT.md              # ← LEER SIEMPRE AL INICIO
├── docs/plan/             # Planes por versión
│   └── v1.0.15-plan.md
├── docs/referencia/
│   └── seguridad-auditoria.md
├── backend/
│   ├── server.py         # API principal
│   ├── config.py         # Configuración
│   └── ...
├── frontend/
│   ├── login.html
│   └── index.html       # Dashboard (~3100 líneas)
└── .env                # Configuración
```

---

## 🔧 Cómo Levantar el Proyecto

### Windows
```powershell
cd AgentEmail-V1
.\ia_env\Scripts\Activate.ps1
python backend\server.py
# URL: http://localhost:8000
```

### macOS/Linux
```bash
cd AgentEmail-V1
source ia_env/bin/activate
python backend/server.py
# URL: http://localhost:8000
```

### Credenciales
- **Email:** admin@airis.com
- **Contraseña:** admin

---

## 📋 Reglas de Nomenclatura

### Cambio de Rama
Al cambiar de rama (ej: v1.0.13 → v1.0.14):
1. Renombrar `docs/plan/v1.0.X-plan.md` → preservar historial
2. Crear `docs/plan/v1.0.Y-plan.md` nuevo
3. Actualizar `frontend/index.html` footer (línea ~641)
4. Actualizar `CONTEXT.md` con nueva rama

### Actualización de Seguridad
- Agregar nuevas recomendaciones en `docs/referencia/seguridad-auditoria.md`
- Actualizar versión en el header del archivo
- Incluir implementación sugerida

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

## 📞 Contacto

| Rol | Nombre | Email |
|-----|--------|-------|
| Desarrollador | Jorge Meneses | jorge.meneses@airis-ae.com.mx |

---

**Última actualización:** 27 de abril de 2026
**Versión:** V1.0.15