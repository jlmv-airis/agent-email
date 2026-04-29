# 📋 README para Asistentes AI - Agent Email AIRIS

**IMPORTANTE:** Si eres un asistente de IA, lee los archivos en este orden antes de empezar cualquier trabajo.

---

## 📖 ORDEN DE LECTURA OBLIGATORIO

### 1. `CONTEXT.md` (LEER PRIMERO)
Este archivo contiene:
- Estado completo del proyecto
- Rama y versión actual
- Arquitectura del sistema
- Cómo levantar el proyecto (Windows/macOS)
- Créditos y contactos

### 2. `AGENTS.md` (LEER SEGUNDO)
Este archivo contiene:
- Tu identidad y rol
- Reglas no negociables
- Tecnologías usadas
- Estados de tickets
- Reglas de nomenclatura

### 3. `docs/plan/[VERSION]-plan.md`
Este archivo contiene:
- Objetivos de la iteración actual
- Tareas completadas
- Pendientes por hacer
- Historial de cambios

---

## 🚀 CÓMO LEVANTAR EL PROYECTO

### Windows
```powershell
# Opción 1: Script automático
powershell -ExecutionPolicy Bypass -File INICIALIZAR-PROYECTO.ps1

# Opción 2: Manual
cd backend
python server.py
```

### macOS/Linux
```bash
# Opción 1: Script automático
bash INICIALIZAR-PROYECTO.sh

# Opción 2: Manual
cd backend
python server.py
```

---

## 📊 ARCHIVOS CLAVE DEL PROYECTO

| Archivo | Propósito |
|---------|-----------|
| `CONTEXT.md` | Estado completo del proyecto |
| `AGENTS.md` | Reglas del asistente AI |
| `docs/plan/v1.0.16-plan.md` | Plan actual |
| `docs/referencia/seguridad-auditoria.md` | Auditoría de seguridad |

---

## 🛠️ STACK TECNOLÓGICO

- **Backend:** Python, Flask, SQLite
- **Frontend:** HTML, TailwindCSS, JavaScript
- **Auth:** JWT tokens
- **Email:** IMAP/SMTP
- **IA:** Gemini API, Groq

---

## 📧 ACCESO

- **URL:** http://localhost:8000
- **Email:** admin@airis.com
- **Contraseña:** admin

---

## 🔧 COMANDOS ÚTILES

### Ver estado del servidor
```powershell
Invoke-WebRequest -Uri "http://localhost:8000/api/health" -UseBasicParsing
```

### Ver logs
```powershell
Get-Content backend/logs/agent-email.log -Tail 50 -Wait
```

### Detener servidor
```powershell
.\DETENER-SISTEMA.ps1
```

---

## 📝 REGLAS NO NEGOCIABLES 

1. **LEER CONTEXT.md** al inicio de cada sesión
2. **LEER AGENTS.md** para conocer tu rol
3. **LEER el plan** de la versión actual
4. **Actualizar el plan** cuando cambies de rama
5. **Actualizar el footer** con la nueva versión
6. **Actualizar seguridad** con nuevas recomendaciones

---

## 📞 CONTACTO

| Rol | Nombre | Email |
|-----|--------|-------|
| Desarrollador | Jorge Meneses | jorge.meneses@airis-ae.com.mx |

---

**Última actualización:** 27 de abril de 2026
**Versión:** V1.0.16
**Rama:** v1.0.16