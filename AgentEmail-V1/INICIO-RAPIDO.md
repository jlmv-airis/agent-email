# 🚀 Guía de Inicio - Agent Email AIRIS V1

## 📌 Descripción Rápida

Este documento explica cómo usar los scripts de control para iniciar, detener y diagnosticar el sistema **Agent Email AIRIS V1**.

---

## 🎯 Opciones de Inicio Rápido

### Opción 1: PowerShell (Recomendado) ⭐

**Ventajas:**
- Mejor manejo de errores
- Validación automática del servidor
- Espera inteligente a que el servidor esté listo
- Mejor presentación visual

**Ejecutar:**
```powershell
powershell -ExecutionPolicy Bypass -File INICIAR-SISTEMA.ps1
```

**O si ya estás en PowerShell:**
```powershell
.\INICIAR-SISTEMA.ps1
```

**Con opciones:**
```powershell
# Saltar instalación de dependencias (más rápido si ya está instalado)
.\INICIAR-SISTEMA.ps1 -SkipInstall

# Usar puerto diferente
.\INICIAR-SISTEMA.ps1 -Port 9000
```

---

### Opción 2: Command Prompt (CMD)

**Ejecutar:**
```cmd
INICIAR-SISTEMA.bat
```

**Ventajas:**
- No requiere PowerShell
- Interfaz simple

---

## 🛑 Detener Servicios

### PowerShell:
```powershell
powershell -ExecutionPolicy Bypass -File DETENER-SISTEMA.ps1
```

**Con fuerza (sin confirmación):**
```powershell
.\DETENER-SISTEMA.ps1 -Force
```

### Command Prompt:
```cmd
DETENER-SISTEMA.bat
```

---

## 🔍 Diagnosticar Problemas

### Verificar estado del sistema:
```powershell
powershell -ExecutionPolicy Bypass -File DIAGNOSTICO.ps1
```

**Información que verás:**
- ✅ Estado del entorno virtual
- ✅ Procesos Python en ejecución
- ✅ Conectividad al servidor
- ✅ Archivos importantes
- ✅ Dependencias instaladas
- ✅ Últimas líneas del log

---

## 📍 Acceso a la Aplicación

```
URL: http://localhost:8000
Email: admin@airis.com
Contraseña: admin123
```

---

## 📊 Ubicaciones de Archivos Importantes

| Archivo | Ubicación | Propósito |
|---------|-----------|----------|
| **Logs** | `backend/logs/agent-email.log` | Evento del servidor |
| **Base de Datos** | `database/agent_email.db` | Datos de la aplicación |
| **.env** | Raíz del proyecto | Configuración |
| **Virtual Env** | `.venv/` | Entorno Python aislado |

---

## 🔧 Configuración Manual (Si necesario)

### Crear el entorno virtual manualmente:
```powershell
python -m venv .venv
```

### Activar el entorno:
```powershell
# PowerShell
.\.venv\Scripts\Activate.ps1

# CMD
.venv\Scripts\activate.bat
```

### Instalar dependencias:
```powershell
pip install -r requirements.txt
python -m pip install python-json-logger flask-limiter
```

### Iniciar servidor manualmente:
```powershell
cd backend
python server.py
```

---

## 📋 Flujo Típico de Uso

```
1. Ejecutar INICIAR-SISTEMA.ps1
   ↓
2. Esperar confirmación "✅ SISTEMA INICIADO EXITOSAMENTE"
   ↓
3. Se abre navegador automáticamente en http://localhost:8000
   ↓
4. Login con admin@airis.com / admin123
   ↓
5. Usar la aplicación
   ↓
6. Para salir: Ejecutar DETENER-SISTEMA.ps1
```

---

## 🐛 Solución de Problemas

### "El puerto 8000 ya está en uso"
```powershell
# Opción 1: Usar diferente puerto
.\INICIAR-SISTEMA.ps1 -Port 9000

# Opción 2: Detener proceso existente
Stop-Process -Name python -Force
```

### "Entorno virtual no encontrado"
```powershell
python -m venv .venv
```

### "ModuleNotFoundError"
```powershell
pip install -r requirements.txt
```

### "Servidor no responde"
```powershell
# Ver logs
Get-Content backend/logs/agent-email.log -Tail 50

# O ejecutar diagnostico
.\DIAGNOSTICO.ps1
```

---

## 💡 Tips Útiles

**Ver logs en tiempo real:**
```powershell
Get-Content backend/logs/agent-email.log -Tail 50 -Wait
```

**Ver procesos Python activos:**
```powershell
Get-Process python | Select-Object Id, ProcessName, WorkingSet
```

**Limpiar caché de Python:**
```powershell
Get-ChildItem -Path . -Include __pycache__ -Recurse -Force | Remove-Item -Recurse -Force
```

---

## 📞 Información de Contacto

Para reportar problemas o sugerencias, contacta al equipo de desarrollo AIRIS.

---

**Última actualización:** 14 de Abril de 2026
**Versión:** 1.0 - Scripts de Control Mejorados
