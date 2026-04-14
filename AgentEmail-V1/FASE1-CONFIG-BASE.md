# 🔧 FASE 1: Configuración Base - Guía de Instalación

## ¿Qué cambió?

### 1. **Configuración Centralizada** (`config.py`)
- ✅ `SECRET_KEY` ahora se carga desde `.env` (no rota en cada reinicio)
- ✅ Variables de ambiente centralizadas
- ✅ Diferenciación por ambiente: `development`, `production`, `testing`
- ✅ Validación automática de configuración crítica

### 2. **Logging Estructurado** (`logger_config.py`)
- ✅ Logs en consola + archivos rotados
- ✅ Formato JSON para integración con herramientas de monitoreo
- ✅ Niveles de log dinámicos por ambiente
- ✅ Archivos con rotación automática (`logs/agent-email.log`)

### 3. **Requirements Pinados**
- ✅ Todas las versiones fijas (reproducibilidad garantizada)
- ✅ Paquetes de desarrollo incluidos (pytest, black, flake8)
- ✅ Nueva dependencia: `python-json-logger` (logging JSON)

### 4. **Docker & Containerización**
- ✅ Multi-stage Dockerfile optimizado
- ✅ docker-compose.yml con:
  - Agent Email (Flask)
  - Redis (caching + rate limiting)
  - PostgreSQL (opcional, para migración futura)
- ✅ Health checks automáticos

### 5. **Archivos de Configuración**
- ✅ `.env.example` - Template para configuración
- ✅ `.env` - Valores de desarrollo (no versionear)
- ✅ `.gitignore` - Excluye secretos y directorio de logs

---

## 🚀 Instalación Rápida

### Paso 1: Activar venv
```powershell
# Windows PowerShell
.\.venv\Scripts\Activate.ps1

# Linux/Mac
source .venv/bin/activate
```

### Paso 2: Instalar nuevas dependencias
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Paso 3: Generar SECRET_KEY seguro
```bash
python -c "import secrets; print('SECRET_KEY='+secrets.token_hex(32))"
```
Copiar salida y actualizar en `.env`:
```
SECRET_KEY=<tu-clave-aqui>
```

### Paso 4: Verificar configuración
```bash
python -c "from backend.config import config; print('✅ Configuración válida')"
```

### Paso 5: Ejecutar servidor
```bash
python backend/server.py
```

Acceder a: **http://localhost:8000**

---

## 🐳 Instalación con Docker

### Opción 1: Docker Compose (Recomendado)
```bash
# Construir imagen
docker-compose build

# Iniciar servicios (includes Redis)
docker-compose up -d

# Ver logs
docker-compose logs -f agent-email
```

### Opción 2: Docker Puro
```bash
# Construir imagen
docker build -t agent-email:latest .

# Ejecutar contenedor
docker run -p 8000:8000 \
  -e ENVIRONMENT=development \
  -e SECRET_KEY=your-secret-key \
  -v $(pwd)/database:/app/database \
  -v $(pwd)/logs:/app/logs \
  agent-email:latest
```

---

## 📦 Estructura de Archivos Nuevos

```
.
├── .env                    # Configuración local (NO versionear)
├── .env.example           # Template de configuración
├── .gitignore             # Excluye secretos y logs
├── Dockerfile             # Multi-stage build
├── docker-compose.yml     # Orquestación de servicios
├── requirements.txt       # Dependencias pinadas
├── backend/
│   ├── config.py         # ✨ NUEVO: Configuración centralizada
│   ├── logger_config.py  # ✨ NUEVO: Logging estructurado
│   └── server.py         # ACTUALIZADO: Usa config.py
└── logs/                 # ✨ NUEVO: Directorio de logs

```

---

## 🔐 Variables de Entorno

| Variable | Descripción | Desarrollo | Producción |
|----------|-------------|------------|-----------|
| `ENVIRONMENT` | Ambiente de ejecución | `development` | `production` |
| `DEBUG` | Modo debug | `False` | `False` |
| `SECRET_KEY` | Clave para JWT | Cambiar | **OBLIGATORIO** |
| `HOST` | IP de escucha | `0.0.0.0` | `0.0.0.0` |
| `PORT` | Puerto | `8000` | `8000` |
| `LOG_LEVEL` | Nivel de logging | `DEBUG` | `WARNING` |
| `CORS_ALLOWED_ORIGINS` | CORS whitelist | localhost | dominio.com |

---

## ✅ Checklist de Validación

- [ ] `.env` creado con `SECRET_KEY` válido
- [ ] `pip install -r requirements.txt` sin errores
- [ ] `from backend.config import config` funciona
- [ ] `python backend/server.py` inicia sin excepciones
- [ ] `curl http://localhost:8000/api/status` retorna `"ok"`
- [ ] `logs/agent-email.log` se crea automáticamente
- [ ] Docker build completado exitosamente

---

## 🐛 Troubleshooting

### Error: "SECRET_KEY" invalido
**Solución:** Generar nueva clave:
```bash
python -c "import secrets; print(secrets.token_hex(32))" >> .env
```

### Error: Cannot find module "config"
**Solución:** Asegurate que estés en el directorio raíz del proyecto y que `.venv` esté activo

### Logs no se crean
**Solución:** Crear manualmente `logs/` directory:
```bash
mkdir logs
```

---

## 📚 Siguiente Fase: FASE 2 (Seguridad)

La Fase 2 incluye:
- [ ] Health check endpoint robusto
- [ ] CORS configuración estricta
- [ ] Rate limiting con Redis
- [ ] Headers de seguridad (Helmet)
- [ ] Input validation mejorada

