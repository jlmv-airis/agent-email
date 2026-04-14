# 🔧 FASE 1: Configuración Base

## ✨ Cambios Implementados

### 🎯 Config Centralizada (`config.py`)
- ✅ `.env` integration
- ✅ 3 profiles: dev/prod/test
- ✅ Validation on startup
- ✅ SECRET_KEY persistence

### 📝 Logging (`logger_config.py`)
- ✅ JSON format (ELK ready)
- ✅ File + console output
- ✅ Auto rotation
- ✅ Dynamic levels

### 🔒 Secrets
- ✅ `.env` + `.env.example`
- ✅ `.gitignore` updated
- ✅ No credentials in VCS

### 📦 Dependencies
- ✅ `requirements.txt` pinned
- ✅ Reproducible builds
- ✅ Dev tools included

### 🐳 Docker
- ✅ Multi-stage Dockerfile
- ✅ `docker-compose.yml`
- ✅ Flask + Redis + PostgreSQL
- ✅ Health checks

---

## 🚀 Quick Start

### 1️⃣ Activate venv
```bash
.\.venv\Scripts\Activate.ps1  # Windows
source .venv/bin/activate      # Linux/Mac
```

### 2️⃣ Install dependencies
```bash
pip install -r requirements.txt
```

### 3️⃣ Generate SECRET_KEY
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

### 4️⃣ Update `.env`
```
SECRET_KEY=<your-key-here>
```

### 5️⃣ Run server
```bash
python backend/server.py
```

🔗 **http://localhost:8000**

---

## 🐳 Docker Setup

### Build
```bash
docker-compose build
```

### Run
```bash
docker-compose up -d
```

### Stop
```bash
docker-compose down
```

---

## 📊 Environment Variables

| Var | Dev | Prod | Note |
|-----|-----|------|------|
| 🌍 ENVIRONMENT | development | production | - |
| 🐛 DEBUG | False | False | Set False always |
| 🔑 SECRET_KEY | - | **REQUIRED** | Generate new |
| 🔌 PORT | 8000 | 8000 | - |
| 📝 LOG_LEVEL | DEBUG | WARNING | - |
| 🔐 CORS | localhost | domain.com | - |

---

## 📁 Structure

```
.
├── .env                    ✔️ Config (local)
├── .env.example           📋 Template
├── requirements.txt       📦 Dependencies
├── Dockerfile             🐳 Container
├── docker-compose.yml     🐘 Orchestration
├── backend/
│   ├── config.py         ⚙️  Config
│   ├── logger_config.py  📝 Logging
│   └── server.py         🚀 App
└── logs/                 📂 Logs dir

```

---

## ✅ Validation Checklist

- [ ] `.env` has SECRET_KEY
- [ ] `pip install -r requirements.txt` OK
- [ ] `python -c "from backend.config import config; print('✅')"` works
- [ ] Server starts: `python backend/server.py`
- [ ] `curl http://localhost:8000/api/status` returns OK
- [ ] `logs/agent-email.log` exists

---

## 🆘 Troubleshooting

### Error: "SECRET_KEY invalid"
```bash
python -c "import secrets; print(secrets.token_hex(32))" >> .env
```

### Error: "Module config not found"
```bash
# Make sure in root directory
# Make sure .venv is active
```

### Logs not created
```bash
mkdir logs
```

---

## 🔮 Next: FASE 2 (Seguridad)

