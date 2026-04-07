# Agente de Email AI - Sistema SaaS de Gestión de Correos

![Versión](https://img.shields.io/badge/version-1.2-blue)
![Python](https://img.shields.io/badge/python-3.8+-green)
![Flask](https://img.shields.io/badge/flask-2.3+-red)
![PostgreSQL](https://img.shields.io/badge/postgresql-15+-blue)

Sistema SaaS de gestión híbrida masiva para correos electrónicos, diseñado para centralizar la operación de **150+ empresas** en una interfaz profesional estilo Gmail, con asistencia de IA (Gemini) y lógica de hilos inteligentes.

---

## 📋 Tabla de Contenidos

- [Características](#-características)
- [Requisitos](#-requisitos)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Instalación Local](#-instalación-local)
  - [Windows](#windows)
  - [macOS](#macos)
  - [Linux](#linux)
- [Configuración de la Base de Datos](#-configuración-de-la-base-de-datos)
- [Configuración del Entorno](#-configuración-del-entorno)
- [Ejecución](#-ejecución)
- [Despliegue en Producción (VPS)](#-despliegue-en-producción-vps)
- [API Endpoints](#-api-endpoints)
- [Solución de Problemas](#-solución-de-problemas)

---

## 🌟 Características

- **Panel Gmail-Pro**: Interfaz administrativa con buscador de empresas y vista densa
- **Gestión de Hilos**: Agrupamiento por `thread_id` para trazabilidad completa
- **Asignación Manual**: Delegar hilos a operadores específicos
- **Base de Datos**: PostgreSQL para persistencia
- **API REST**: Endpoints para gestión de operadores y empresas
- **Soporte IA**: Integración con Gemini para sugerencias
- **Dark Mode**: Soporte completo para modo oscuro
- **CRUD Completo**: Gestión visual de operadores y empresas

---

## 📦 Requisitos

### Software Necesario

| Software | Versión Mínima | Descarga |
|----------|---------------|----------|
| Python | 3.8+ | [python.org](https://www.python.org/downloads/) |
| PostgreSQL | 15+ | [postgresql.org](https://www.postgresql.org/download/) |
| Git | 2.0+ | [git-scm.com](https://git-scm.com/downloads) |

### Opcional (para desarrollo)

| Software | Uso |
|----------|-----|
| Docker | Contenedores |
| pgAdmin | Gestión visual de PostgreSQL |
| VS Code | Editor de código |

---

## 📂 Estructura del Proyecto

```
agent-email/
├── Code/                    # Workflows n8n + Docker
│   └── n8n-local/         # Docker Compose para n8n
├── Mockup/                 # Diseños e infografías
├── Panel.html              # Panel administrativo principal
├── server.py               # API Flask
├── login.html             # Página de login
├── index.html             # Página principal
├── requirements.txt       # Dependencias Python
├── .env.example          # Variables de entorno ejemplo
├── .env                  # Variables de entorno (no commitear)
├── Setup-AsesoriasIA.ps1  # Script de configuración Windows
├── PROGRESO.md            # Seguimiento del proyecto
└── README.md              # Este archivo
```

---

## 🔧 Instalación Local

### Windows

#### Paso 1: Instalar Python

1. Descarga Python desde [python.org](https://www.python.org/downloads/windows/)
2. **Importante**: Marca "Add Python to PATH"
3. Verifica instalación:
```powershell
python --version
pip --version
```

#### Paso 2: Instalar PostgreSQL

**Opción A: Usando installer**
1. Descarga desde [postgresql.org](https://www.postgresql.org/download/windows/)
2. Instala con pgAdmin
3. Anota la contraseña del usuario `postgres`

**Opción B: Usando Docker**
```powershell
docker run -d --name postgres `
  -e POSTGRES_PASSWORD=tu_password `
  -e POSTGRES_DB=n8n_db `
  -p 5432:5432 `
  postgres:15
```

#### Paso 3: Clonar el Proyecto

```powershell
# Abrir PowerShell o CMD
cd C:\Proyectos
git clone https://github.com/tu-usuario/agent-email.git
cd agent-email
```

#### Paso 4: Crear Entorno Virtual e Instalar Dependencias

```powershell
# Crear entorno virtual
python -m venv venv

# Activar entorno
.\venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt
```

#### Paso 5: Configurar Variables de Entorno

```powershell
# Crear archivo .env
copy .env.example .env

# Editar con tu editor favorito
notepad .env
```

Contenido del `.env`:
```env
DATABASE_URL=postgresql://postgres:tu_password@localhost:5432/n8n_db
N8N_URL=http://localhost:5678
PORT=8000
FLASK_DEBUG=True
```

#### Paso 6: Crear Base de Datos

```powershell
# Conectar a PostgreSQL
psql -U postgres -h localhost

# En psql, ejecutar:
CREATE DATABASE n8n_db;
\q
```

#### Paso 7: Iniciar Servidor

```powershell
python server.py
```

---

### macOS

#### Paso 1: Instalar Homebrew (si no lo tienes)

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

#### Paso 2: Instalar Python y PostgreSQL

```bash
# Actualizar Homebrew
brew update

# Instalar Python y PostgreSQL
brew install python@3.11 postgresql@15
```

#### Paso 3: Iniciar PostgreSQL

```bash
# Iniciar servicio
brew services start postgresql@15

# Crear usuario y base de datos
createuser -s postgres
createdb n8n_db
```

#### Paso 4: Clonar el Proyecto

```bash
cd ~/Proyectos
git clone https://github.com/tu-usuario/agent-email.git
cd agent-email
```

#### Paso 5: Crear Entorno Virtual

```bash
# Crear entorno virtual
python3 -m venv venv

# Activar entorno
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

#### Paso 6: Configurar Variables de Entorno

```bash
# Copiar archivo de ejemplo
cp .env.example .env

# Editar
nano .env
```

```env
DATABASE_URL=postgresql://postgres:@localhost:5432/n8n_db
N8N_URL=http://localhost:5678
PORT=8000
FLASK_DEBUG=True
```

#### Paso 7: Iniciar Servidor

```bash
python server.py
```

---

### Linux (Ubuntu/Debian)

#### Paso 1: Actualizar Sistema e Instalar Dependencias

```bash
# Actualizar
sudo apt update && sudo apt upgrade -y

# Instalar Python, PostgreSQL y herramientas
sudo apt install -y python3 python3-pip python3-venv postgresql postgresql-contrib git
```

#### Paso 2: Configurar PostgreSQL

```bash
# Iniciar servicio
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Crear usuario y base de datos
sudo -u postgres psql -c "CREATE DATABASE n8n_db;"
sudo -u postgres psql -c "CREATE USER n8n_user WITH PASSWORD 'n8n_password';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE n8n_db TO n8n_user;"
sudo -u postgres psql -c "ALTER DATABASE n8n_db OWNER TO n8n_user;"
```

#### Paso 3: Clonar el Proyecto

```bash
cd ~/Proyectos
git clone https://github.com/tu-usuario/agent-email.git
cd agent-email
```

#### Paso 4: Crear Entorno Virtual

```bash
# Crear entorno virtual
python3 -m venv venv

# Activar entorno
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

#### Paso 5: Configurar Variables de Entorno

```bash
# Copiar archivo de ejemplo
cp .env.example .env

# Editar
nano .env
```

```env
DATABASE_URL=postgresql://n8n_user:n8n_password@localhost:5432/n8n_db
N8N_URL=http://localhost:5678
PORT=8000
FLASK_DEBUG=True
```

#### Paso 6: Iniciar Servidor

```bash
python server.py
```

---

## 🗄️ Configuración de la Base de Datos

### Tablas Necesarias

Ejecuta este SQL en PostgreSQL para crear las tablas:

```sql
-- Tabla de usuarios/operadores
CREATE TABLE IF NOT EXISTS usuarios (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    nombre VARCHAR(100),
    email VARCHAR(255),
    password_hash VARCHAR(255),
    rol VARCHAR(20) DEFAULT 'operador',
    notas TEXT,
    activo BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de empresas
CREATE TABLE IF NOT EXISTS empresas (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    alias VARCHAR(100),
    imap_host VARCHAR(255),
    imap_port INTEGER DEFAULT 993,
    email_user VARCHAR(255),
    email_pass VARCHAR(255),
    smtp_host VARCHAR(255),
    smtp_port INTEGER DEFAULT 465,
    logo_url TEXT,
    activo BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de configuración
CREATE TABLE IF NOT EXISTS configuracion (
    clave VARCHAR(50) PRIMARY KEY,
    valor VARCHAR(255)
);

-- Tabla de grupos
CREATE TABLE IF NOT EXISTS grupos (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100),
    color VARCHAR(20),
    tipo VARCHAR(20)
);

-- Tabla de mensajes
CREATE TABLE IF NOT EXISTS mensajes_entrantes (
    id SERIAL PRIMARY KEY,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    remitente VARCHAR(255),
    asunto TEXT,
    mensaje TEXT,
    thread_id VARCHAR(100),
    cuenta_empresa VARCHAR(255),
    leido BOOLEAN DEFAULT FALSE,
    de_operador BOOLEAN DEFAULT FALSE,
    asignado_a VARCHAR(50)
);

-- Insertar configuración inicial
INSERT INTO configuracion (clave, valor) VALUES ('caducidad_hilos_dias', '7')
ON CONFLICT (clave) DO NOTHING;
```

### Comando rápido para crear tablas

```bash
# Ejecutar SQL desde archivo
psql -U postgres -d n8n_db -f schema.sql
```

---

## ⚙️ Configuración del Entorno

### Variables de Entorno

| Variable | Descripción | Ejemplo |
|----------|-------------|---------|
| `DATABASE_URL` | URL de PostgreSQL | `postgresql://user:pass@localhost:5432/db` |
| `N8N_URL` | URL de n8n | `http://localhost:5678` |
| `PORT` | Puerto del servidor | `8000` |
| `FLASK_DEBUG` | Modo debug | `True` / `False` |

### Archivo .env

Crea un archivo `.env` en la raíz del proyecto:

```env
# Base de datos
DATABASE_URL=postgresql://n8n_user:n8n_password@localhost:5432/n8n_db

# n8n
N8N_URL=http://localhost:5678

# Servidor
PORT=8000
FLASK_DEBUG=True
```

**⚠️ Importante**: Nunca subas el archivo `.env` a Git. Ya está incluido en `.gitignore`.

---

## 🚀 Ejecución

### Desarrollo Local

```bash
# Activar entorno virtual
# Windows:
.\venv\Scripts\activate

# macOS/Linux:
source venv/bin/activate

# Iniciar servidor
python server.py
```

### URLs de Acceso

| Servicio | URL |
|----------|-----|
| Panel Admin | http://localhost:8000/Panel.html |
| Login | http://localhost:8000/login.html |
| Página Principal | http://localhost:8000/index.html |
| API Status | http://localhost:8000/api/status |

### Credenciales por Defecto

| Usuario | Contraseña |
|---------|------------|
| `admin` | `admin` |

---

## 🌐 Despliegue en Producción (VPS)

### Paso 1: Configurar VPS (Hostgator/Ubuntu)

```bash
# Conectar por SSH
ssh root@tu-ip-del-servidor

# Actualizar sistema
apt update && apt upgrade -y

# Instalar dependencias
apt install -y python3 python3-pip python3-venv postgresql postgresql-contrib nginx certbot python3-certbot-nginx git
```

### Paso 2: Configurar PostgreSQL

```bash
# Crear usuario y base de datos
sudo -u postgres psql
CREATE DATABASE n8n_db;
CREATE USER n8n_user WITH PASSWORD 'tu_password_fuerte';
GRANT ALL PRIVILEGES ON DATABASE n8n_db TO n8n_user;
\q
```

### Paso 3: Desplegar Aplicación

```bash
# Crear usuario para la aplicación
useradd -m -s /bin/bash agentemail
usermod -aG sudo agentemail

# Crear directorio
mkdir -p /var/www/agentemail
cd /var/www/agentemail

# Clonar repositorio (como el usuario)
git clone https://github.com/tu-usuario/agent-email.git .
chown -R agentemail:agentemail /var/www/agentemail

# Cambiar a usuario
su - agentemail
cd /var/www/agentemail

# Crear entorno virtual
python3 -m venv venv
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
pip install gunicorn
```

### Paso 4: Configurar Gunicorn (Systemd)

```bash
# Crear archivo de servicio
sudo nano /etc/systemd/system/agentemail.service
```

Contenido:
```ini
[Unit]
Description=Agent Email API
After=network.target postgresql.service

[Service]
User=agentemail
Group=agentemail
WorkingDirectory=/var/www/agentemail
Environment="PATH=/var/www/agentemail/venv/bin"
Environment="DATABASE_URL=postgresql://n8n_user:tu_password@localhost:5432/n8n_db"
ExecStart=/var/www/agentemail/venv/bin/gunicorn -w 4 -b 127.0.0.1:8000 server:app --timeout 120
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

```bash
# Habilitar e iniciar servicio
sudo systemctl daemon-reload
sudo systemctl enable agentemail
sudo systemctl start agentemail
```

### Paso 5: Configurar Nginx (Proxy Reverso)

```bash
sudo nano /etc/nginx/sites-available/agentemail
```

Contenido:
```nginx
server {
    listen 80;
    server_name agentemail.tudominio.com;

    client_max_body_size 100M;

    location / {
        root /var/www/agentemail;
        try_files $uri $uri/ =404;
    }

    location /api/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /n8n/ {
        proxy_pass http://127.0.0.1:5678/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

```bash
# Habilitar sitio
sudo ln -s /etc/nginx/sites-available/agentemail /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### Paso 6: SSL con Let's Encrypt

```bash
sudo certbot --nginx -d agentemail.tudominio.com
sudo systemctl restart nginx
```

### Paso 7: Instalar n8n (Opcional)

```bash
# Como usuario agentemail
su - agentemail
cd ~

# Instalar n8n globalmente
npm install -g n8n

# Crear servicio systemd para n8n
sudo nano /etc/systemd/system/n8n.service
```

```ini
[Unit]
Description=n8n
After=network.target

[Service]
User=agentemail
Type=simple
ExecStart=/usr/bin/n8n start
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable n8n
sudo systemctl start n8n
```

---

## 🔌 API Endpoints

### Operadores

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/operadores` | Listar todos los operadores |
| POST | `/api/operadores` | Crear nuevo operador |
| PUT | `/api/operadores/<username>` | Actualizar operador |
| DELETE | `/api/operadores/<username>` | Eliminar operador |

### Empresas

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/empresas` | Listar todas las empresas |
| POST | `/api/empresas` | Crear nueva empresa |
| PUT | `/api/empresas/<id>` | Actualizar empresa |
| DELETE | `/api/empresas/<id>` | Eliminar empresa |

### Configuración

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/config` | Obtener toda la configuración |
| GET | `/api/config/<key>` | Obtener valor específico |
| PUT | `/api/config/<key>` | Guardar valor |

### Sistema

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/status` | Estado del servicio |
| GET | `/health` | Health check |

---

## 🔧 Solución de Problemas

### Error: "Module not found"

```bash
# Reinstalar dependencias
pip install -r requirements.txt --force-reinstall
```

### Error: "Connection refused" en PostgreSQL

```bash
# Verificar que PostgreSQL está corriendo
sudo systemctl status postgresql

# Reiniciar si es necesario
sudo systemctl restart postgresql
```

### Error: "Port already in use"

```bash
# Ver qué está usando el puerto
sudo lsof -i :8000

# Matar el proceso o usar otro puerto
PORT=8001 python server.py
```

### Error: "Database does not exist"

```bash
# Conectar a PostgreSQL
sudo -u postgres psql

# Crear base de datos
CREATE DATABASE n8n_db;
\q
```

### Error: "Permission denied" en Linux

```bash
# Dar permisos a la carpeta del proyecto
sudo chown -R $USER:$USER /var/www/agentemail
chmod -R 755 /var/www/agentemail
```

---

## 📊 Monitoreo

### Ver logs del servicio

```bash
# Gunicorn/Flask
sudo journalctl -u agentemail -f

# n8n
sudo journalctl -u n8n -f

# Nginx
sudo tail -f /var/log/nginx/error.log
```

### Verificar estado de servicios

```bash
sudo systemctl status agentemail
sudo systemctl status n8n
sudo systemctl status nginx
sudo systemctl status postgresql
```

---

## 📝 Licencia

Este proyecto es propiedad de **AIRIS AI Team**.

---

**Versión**: 1.2  
**Última actualización**: 2024
