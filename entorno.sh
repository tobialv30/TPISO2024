#!/bin/bash

# Unicamente para sistemas Unix
# lo que hace es verificar que exista el directorio venv/ y si no existe debemos crearlo y activarlo
# si ya existe solo lo activamos

#----------------------------------------------

# Variables
# Variables de colores

readonly RED='\033[0;31m'
readonly GREEN='\033[0;32m'
readonly YELLOW='\033[0;33m'
readonly END='\033[0m'
readonly CYAN='\033[0;36m'
readonly BLUE='\033[0;34m'
readonly PURPLE='\033[0;35m'
readonly WHITE='\033[0;37m'
readonly BLACK='\033[0;30m'
readonly BOLD='\033[1m'
readonly UNDERLINE='\033[4m'

function ctrl_c() {
    echo -e "\n${RED}[-]${END} ${BOLD}Saliendo del entorno virtual${END}"
    deactivate
    exit 0
}

trap ctrl_c INT


echo -e "${CYAN}[+]${END} ${BOLD}Activador de entorno virtual${END}"



# Verificamos si existe el directorio venv/
if [ -d "venv" ]; then
    echo -e "${GREEN}[+]${END} ${BOLD}Activando entorno virtual${END}"
    sleep 1
    source venv/bin/activate
    clear
    echo -e "${YELLOW}[+]${END} ${GREEN}Entorno virtual activado${END}"
else
    echo -e "${YELLOW}[+]${END} ${BOLD}Creando entorno virtual${END}"
    python -m venv venv
    clear

    echo -e "${GREEN}[+]${END} ${BOLD}Activando entorno virtual${END}"
    source venv/bin/activate
    
    echo -e "${YELLOW}[+]${END} ${GREEN}Actualizando pip${END}"
    pip install --upgrade pip
    clear

    echo -e "${YELLOW}[+]${END} ${GREEN}Instalando requerimientos${END}"
    pip install -r requirements.txt

    clear
    echo -e "${YELLOW}[+]${END} ${GREEN}Entorno virtual creado y activado${END}"
fi