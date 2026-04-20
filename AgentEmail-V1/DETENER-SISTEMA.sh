#!/bin/bash

# Configuración de colores
CYAN='\033[0;36m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${CYAN}==========================================${NC}"
echo -e "${CYAN}  AGENT EMAIL AIRIS V1 - DETENCIÓN${NC}"
echo -e "${CYAN}==========================================${NC}"

# Buscar procesos de Python ejecutando server.py
PIDS=$(ps aux | grep "[p]ython.*server.py" | awk '{print $2}')

if [ -z "$PIDS" ]; then
    echo -e "${YELLOW}No se encontraron procesos del servidor ejecutándose.${NC}"
    exit 0
fi

echo -e "Procesos encontrados: $PIDS"

for pid in $PIDS; do
    echo -e "==> ${CYAN}Deteniendo proceso $pid...${NC}"
    kill -15 "$pid" 2>/dev/null
    sleep 1
    if kill -0 "$pid" 2>/dev/null; then
        kill -9 "$pid"
    fi
    echo -e "${GREEN}Proceso $pid detenido.${NC}"
done

echo -e "${GREEN}Todos los servicios se han detenido correctamente.${NC}"
