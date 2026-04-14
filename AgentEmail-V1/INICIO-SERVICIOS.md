# 🎯 GUÍA RÁPIDA - Levantar Agent Email AIRIS V1

## ⚡ Lo Más Rápido (3 pasos)

### Opción A: Con PowerShell (Recomendado)
```powershell
powershell -ExecutionPolicy Bypass -File INICIAR-SISTEMA.ps1
```

### Opción B: Con Command Prompt
```cmd
INICIAR-SISTEMA.bat
```

**¡Listo!** El navegador se abrirá automáticamente en:
```
http://localhost:8000
```

---

## 👤 Credenciales por Defecto

```
Email: admin@airis.com
Contraseña: admin123
```

---

## 📊 Scripts Disponibles

| Script | Función | Cómo ejecutar |
|--------|---------|---------------|
| **INICIAR-SISTEMA.ps1** | Levanta todos los servicios | `powershell -ExecutionPolicy Bypass -File INICIAR-SISTEMA.ps1` |
| **INICIAR-SISTEMA.bat** | Levanta todos los servicios (CMD) | Doble clic o `INICIAR-SISTEMA.bat` |
| **DETENER-SISTEMA.ps1** | Detiene los servicios | `powershell -ExecutionPolicy Bypass -File DETENER-SISTEMA.ps1` |
| **DETENER-SISTEMA.bat** | Detiene los servicios (CMD) | Doble clic o `DETENER-SISTEMA.bat` |
| **DIAGNOSTICO.ps1** | Verifica estado del sistema | `powershell -ExecutionPolicy Bypass -File DIAGNOSTICO.ps1` |
| **INICIO-RAPIDO.md** | Guía completa de uso | Abrir en editor |

---

## ⚙️ Opciones Avanzadas

### Usar un puerto diferente
```powershell
.\INICIAR-SISTEMA.ps1 -Port 9000
```

### Saltar instalación de paquetes (más rápido)
```powershell
.\INICIAR-SISTEMA.ps1 -SkipInstall
```

### Detener servicios sin confirmación
```powershell
.\DETENER-SISTEMA.ps1 -Force
```

---

## 🔍 Diagnosticar Problemas

```powershell
powershell -ExecutionPolicy Bypass -File DIAGNOSTICO.ps1
```

Verifica:
- ✅ Entorno virtual
- ✅ Procesos Python
- ✅ Conectividad al servidor
- ✅ Archivos importantes
- ✅ Dependencias

---

## 📁 Ubicaciones Importantes

```
backend/
  ├── server.py         (Aplicación Flask)
  ├── logs/             (Logs del servidor)
  │   └── agent-email.log
  └── database/         (Base de datos SQLite)
     └── agent_email.db

frontend/
  ├── login.html        (Página de login)
  └── index.html        (Dashboard principal)

.env                     (Configuración)
requirements.txt        (Dependencias Python)
```

---

## 🐛 Solución Rápida de Problemas

### Puerto 8000 ya está en uso
```powershell
# Usar diferente puerto
.\INICIAR-SISTEMA.ps1 -Port 9000
```

### Entorno virtual no existe
```powershell
python -m venv .venv
```

### Paquetes faltantes
```powershell
pip install -r requirements.txt
```

### Ver logs en tiempo real
```powershell
Get-Content backend/logs/agent-email.log -Tail 50 -Wait
```

---

## 💾 Información de Archivos

- **URL de Acceso:** http://localhost:8000
- **Email Admin:** admin@airis.com
- **Contraseña:** admin123
- **Base de Datos:** SQLite (database/agent_email.db)
- **Python Version:** 3.10+
- **Logs:** backend/logs/agent-email.log

---

**Última actualización:** 14 de Abril de 2026 | Versión 1.0
