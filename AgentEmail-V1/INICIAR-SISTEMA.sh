#!/bin/bash

# Configuración de colores
CYAN='\033[0;36m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

PORT=8000
SKIP_INSTALL=false

# Procesar argumentos
while [[ "$#" -gt 0 ]]; do
    case $1 in
        --skip-install) SKIP_INSTALL=true ;;
        --port) PORT="$2"; shift ;;
        *) echo "Opción desconocida: $1"; exit 1 ;;
    esac
    shift
done

echo -e "${CYAN}==========================================${NC}"
echo -e "${CYAN}  AGENT EMAIL AIRIS V1 - INICIO MACOS${NC}"
echo -e "${CYAN}==========================================${NC}"
echo -e "Puerto: $PORT"
echo -e "Fecha: $(date '+%Y-%m-%d %H:%M:%S')"
echo ""

# Verificar Python
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}ERROR: No se encontró 'python3'. Instálalo con 'brew install python'.${NC}"
    exit 1
fi

# Directorios
PROJECT_ROOT=$(pwd)
BACKEND_DIR="$PROJECT_ROOT/backend"
VENV_DIR="$PROJECT_ROOT/.venv"

# Entorno Virtual
if [ ! -d "$VENV_DIR" ]; then
    echo -e "==> ${CYAN}Creando entorno virtual (.venv)...${NC}"
    python3 -m venv .venv
fi

source "$VENV_DIR/bin/activate"

# Instalación de dependencias
if [ "$SKIP_INSTALL" = false ]; then
    echo -e "==> ${CYAN}Actualizando pip e instalando dependencias...${NC}"
    pip install --upgrade pip --quiet
    if [ -f "requirements.txt" ]; then
        pip install -r requirements.txt --quiet
    fi
    pip install requests python-json-logger flask-limiter pytest pytest-cov --quiet
fi

# Verificar puerto
if lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null ; then
    PID=$(lsof -ti :$PORT)
    echo -e "${YELLOW}AVISO: El puerto $PORT ya está en uso por el PID: $PID${NC}"
    echo -e "${RED}Libera el puerto o elige otro con --port [numero].${NC}"
    exit 1
fi

# Iniciar servidor
echo -e "==> ${CYAN}Iniciando servidor Flask en segundo plano...${NC}"
export PORT=$PORT
export PYTHONUNBUFFERED=1

cd "$BACKEND_DIR" || exit
python3 server.py > ../logs/server.log 2>&1 &
SERVER_PID=$!

echo -e "${GREEN}Servidor iniciado (PID: $SERVER_PID)${NC}"

# Esperar a que el servidor responda
echo -e "==> ${CYAN}Esperando a que el servidor esté listo...${NC}"
MAX_ATTEMPTS=15
ATTEMPT=0
READY=false

while [ $ATTEMPT -lt $MAX_ATTEMPTS ]; do
    if curl -s "http://localhost:$PORT" > /dev/null; then
        READY=true
        break
    fi
    sleep 1
    ATTEMPT=$((ATTEMPT+1))
done

if [ "$READY" = true ]; then
    echo -e "${GREEN}SISTEMA INICIADO EXITOSAMENTE${NC}"
    echo -e "URL: ${CYAN}http://localhost:$PORT${NC}"
    open "http://localhost:$PORT"
else
    echo -e "${YELLOW}El servidor tarda en responder. Revisa logs/server.log${NC}"
fi
