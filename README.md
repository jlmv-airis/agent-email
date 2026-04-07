# Agente de Email AI - Consola de Administración Global (V 1.2)

Sistema SaaS de gestión híbrida masiva para correos electrónicos, diseñado para centralizar la operación de más de **150 empresas** en una interfaz profesional estilo Gmail, con asistencia de IA (Gemini) y lógica de hilos inteligentes.

## 🌟 Características
- **Panel Gmail-Pro:** Interfaz administrativa con buscador de empresas y vista densa
- **Gestión de Hilos:** Agrupamiento por `thread_id` para trazabilidad completa
- **Asignación Manual:** Delegar hilos a operadores específicos
- **Base de Datos:** PostgreSQL compartido con n8n
- **API REST:** Endpoints para gestión de operadores
- **Soporte IA:** Integración con Gemini para sugerencias

---

## 🚀 Despliegue en Hosting (Hostgator/Ubuntu)

### 1. Preparar el Servidor
```bash
# Actualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar dependencias
sudo apt install -y python3 python3-pip python3-venv nginx certbot python3-certbot-nginx
```

### 2. Configurar PostgreSQL (de n8n)
```bash
# Conectar a PostgreSQL de n8n
sudo -u postgres psql -d n8n_db

# Ejecutar en SQL:
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

CREATE TABLE IF NOT EXISTS grupos (id SERIAL PRIMARY KEY, nombre VARCHAR(100), color VARCHAR(20), tipo VARCHAR(20));
CREATE TABLE IF NOT EXISTS configuracion (clave VARCHAR(50) PRIMARY KEY, valor VARCHAR(255));
\q
```

### 3. Desplegar Aplicación
```bash
cd /var/www/agent-email

# Crear entorno virtual
python3 -m venv venv
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Crear archivo .env
cp .env.example .env
# Editar .env con credenciales de PostgreSQL
nano .env
```

### 4. Configurar Gunicorn + Systemd
```bash
# Crear servicio systemd
sudo nano /etc/systemd/system/agent-email.service
```

Contenido del servicio:
```ini
[Unit]
Description=Agent Email API
After=network.target

[Service]
User=www-data
WorkingDirectory=/var/www/agent-email
Environment="PATH=/var/www/agent-email/venv/bin"
ExecStart=/var/www/agent-email/venv/bin/gunicorn -w 4 -b 127.0.0.1:8000 server:app
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable agent-email
sudo systemctl start agent-email
```

### 5. Configurar Nginx (Proxy Reverso)
```bash
sudo nano /etc/nginx/sites-available/agent-email
```

Contenido:
```nginx
server {
    listen 80;
    server_name agentemail.tudominio.com;

    location / {
        root /var/www/agent-email;
        try_files $uri $uri/ =404;
    }

    location /api/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /n8n/ {
        proxy_pass http://127.0.0.1:5678/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

```bash
sudo ln -s /etc/nginx/sites-available/agent-email /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### 6. SSL (Let's Encrypt)
```bash
sudo certbot --nginx -d agentemail.tudominio.com
```

### 7. Docker + n8n (si no está instalado)
```bash
cd /var/www/agent-email/Code/n8n-local
docker-compose up -d
```

---

## 📂 Estructura del Proyecto
```
agent-email/
├── Code/                    # Workflows n8n + Docker
│   └── n8n-local/          # Docker Compose para n8n
├── Panel.html              # Panel administrativo
├── server.py               # API Flask
├── requirements.txt        # Dependencias Python
├── .env.example           # Variables de entorno
└── README.md
```

## 🔌 API Endpoints
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/status` | Estado del servicio |
| GET | `/api/operadores` | Listar operadores |
| POST | `/api/operadores` | Crear operador |
| PUT | `/api/operadores/<username>` | Actualizar |
| DELETE | `/api/operadores/<username>` | Eliminar (soft delete) |
| GET/PUT | `/api/config/<key>` | Configuración |

## 🔐 Credenciales por Defecto
- **Panel Admin:** `admin` / `admin`
- **Base de datos:** Usar las de n8n en `.env`

---
**Desarrollado por:** AIRIS AI Team  
**Estado:** En Desarrollo (v0.1.0)
