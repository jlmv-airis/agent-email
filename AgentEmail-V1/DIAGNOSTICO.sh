#!/bin/bash

# Configuración de colores
CYAN='\033[0;36m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${CYAN}==========================================${NC}"
echo -e "${CYAN}  AGENT EMAIL AIRIS V1 - DIAGNÓSTICO${NC}"
echo -e "${CYAN}==========================================${NC}"

# Verificar Python
echo -e "[PYTHON] Versión:"
python3 --version 2>&1 | sed 's/^/  /'

# Verificar Entorno Virtual
echo -e "\n[VENV] Estado:"
if [ -d ".venv" ]; then
    echo -e "  ${GREEN}OK - .venv encontrado${NC}"
else
    echo -e "  ${RED}FALTA - .venv no existe${NC}"
fi

# Verificar Procesos
echo -e "\n[SERVER] Procesos en ejecución:"
ps aux | grep "[p]ython.*server.py" | sed 's/^/  /'
if [ $? -ne 0 ]; then
    echo -e "  ${YELLOW}Ningún proceso detectado.${NC}"
fi

# Verificar Puerto 8000
echo -e "\n[PORT] Conectividad (Puerto 8000):"
if lsof -Pi :8000 -sTCP:LISTEN -t >/dev/null ; then
    echo -e "  ${GREEN}OK - El puerto 8000 está en escucha.${NC}"
else
    echo -e "  ${RED}FALTA - Puerto 8000 cerrado.${NC}"
fi

# Verificar Archivos Clave
echo -e "\n[FILES] Archivos Críticos:"
for file in "backend/server.py" "backend/config.py" ".env.example" "requirements.txt"; do
    if [ -f "$file" ]; then
        echo -e "  ${GREEN}OK - $file${NC}"
    else
        echo -e "  ${RED}FALTA - $file${NC}"
    fi
done

echo -e "\n${CYAN}==========================================${NC}"
echo -e "Diagnóstico completado."
