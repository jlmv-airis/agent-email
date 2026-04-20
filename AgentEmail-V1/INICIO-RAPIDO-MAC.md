# 🚀 Guía de Inicio - Agent Email AIRIS V1 (macOS)

## 📌 Descripción Rápida

Este documento explica cómo iniciar, detener y diagnosticar el sistema **Agent Email AIRIS V1** (versión refactorizada sin n8n) en un entorno macOS.

---

## 🎯 Opciones de Inicio Rápido

### Opción 1: Terminal con Bash (Recomendado) ⭐

**Ventajas:**

- Mejor manejo de errores
- Validación automática del servidor
- Espera inteligente a que el servidor esté listo
- Compatible con zsh/bash

**Ejecutar:**

```bash
# Desde el directorio del proyecto
bash INICIAR-SISTEMA.sh
```

**O directamente:**

```bash
./INICIAR-SISTEMA.sh
```

**Con opciones:**

```bash
# Saltar instalación de dependencias (más rápido si ya está instalado)
./INICIAR-SISTEMA.sh --skip-install

# Usar puerto diferente
./INICIAR-SISTEMA.sh --port 9000
```

---

### Opción 2: Inicio Manual

**Ejecutar paso a paso:**

```bash
# 1. Activar entorno virtual (si existe)
source venv/bin/activate

# 2. Instalar dependencias (si es necesario)
pip install -r requirements.txt

# 3. Iniciar servidor
cd backend
python server.py
```

---

## 🛑 Detener Servicios

### Terminal:

```bash
# Desde el directorio del proyecto
bash DETENER-SISTEMA.sh
```

**Con fuerza (sin confirmación):**

```bash
./DETENER-SISTEMA.sh --force
```

**O manualmente:**

```bash
# Encontrar proceso Python
ps aux | grep python

# Matar proceso (reemplaza PID)
kill -9 <PID>
```

---

## 🔍 Diagnosticar Problemas

### Verificar estado del sistema:

```bash
bash DIAGNOSTICO.sh
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

| Archivo/Directorio | Ubicación                 | Descripción                   |
| ------------------ | ------------------------- | ----------------------------- |
| Base de datos      | `database/agent_email.db` | SQLite local                  |
| Logs               | `logs/`                   | Archivos de log del sistema   |
| Configuración      | `backend/.env`            | Variables de entorno          |
| Servidor           | `backend/server.py`       | Código principal del servidor |
| Frontend           | `frontend/`               | Archivos HTML/CSS/JS          |

---

## 🛠️ Requisitos Previos para macOS

### Instalar Homebrew (si no lo tienes):

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### Instalar Python:

```bash
brew install python@3.11
```

### Instalar dependencias del proyecto:

```bash
pip install -r requirements.txt
```

---

## 🔧 Solución de Problemas Comunes en macOS

### Error de puerto ocupado:

```bash
# Ver qué usa el puerto 8000
lsof -i :8000

# Matar proceso
kill -9 <PID>
```

### Error de permisos:

```bash
# Dar permisos de ejecución a scripts
chmod +x *.sh
```

### Error de dependencias:

```bash
# Actualizar pip
pip install --upgrade pip

# Reinstalar dependencias
pip install -r requirements.txt --force-reinstall
```

---

## 📞 Soporte

Si encuentras problemas específicos de macOS, consulta:

- `ROL-AI.md` - Rol del asistente AI
- `v1.0.11-mac.md` - Checklist de mejoras para esta rama
- Logs en `logs/` para diagnóstico detallado
