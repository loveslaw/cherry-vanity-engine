#!/usr/bin/env bash

# aqxilorcore - Linux & Chromebook (Chrome OS) Launcher
cd "$(dirname "$0")"

GREEN='\033[0;32m'
RED='\033[0;31m'
MAGENTA='\033[0;35m'
NC='\033[0m'

echo -e "${MAGENTA}====================================================${NC}"
echo -e "${MAGENTA}   aqxilorcore - Ultra-Fast Vanity Engine          ${NC}"
echo -e "${MAGENTA}====================================================${NC}"

# Check for python3
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}[ERROR] Python3 is not installed!${NC}"
    echo "On Chromebook / Ubuntu / Debian, run:"
    echo "  sudo apt update && sudo apt install -y python3 python3-pip"
    exit 1
fi

# Install requirements
echo -e "${GREEN}[*] Verifying dependencies...${NC}"
python3 -m pip install -r requirements.txt --quiet --break-system-packages 2>/dev/null || python3 -m pip install -r requirements.txt --quiet

# Launch single-file standalone edition
echo -e "${GREEN}[*] Starting aqxilorcore...${NC}"
python3 vanity.py
