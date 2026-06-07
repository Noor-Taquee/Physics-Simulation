#!/bin/bash

# Custom colors
LIGHT_BLUE='\033[1;36m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0;m' # No Color

echo -e "${LIGHT_BLUE}Starting Physics-Simulation Installer Wizard...${NC}\n"

# Tracking variables for dependencies
MISSING_PACKAGES=()

# 1. CORE PYTHON3 CHECK
echo -e "${YELLOW}[1/5] Checking Python3 Core...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Python3 is not installed on this system.${NC}"
    read -p "Would you like to install python3 now? (y/n): " install_py
    if [[ "$install_py" =~ ^[Yy]$ ]]; then
        echo -e "Fetching python3...${NC}"
        sudo apt update && sudo apt install python3 -y
    else
        echo -e "${RED}Aborting setup: Python 3 is strictly required.${NC}"
        exit 1
    fi
else
    echo -e "${GREEN}Python3 core is ready!${NC}"
fi

# 2. GRANULAR PIP & VENV VALIDATION
echo -e "\n${YELLOW}[2/5] Scanning Environment Subsystems...${NC}"

# Check pip
if ! command -v pip3 &> /dev/null && ! python3 -m pip --version &> /dev/null; then
    echo -e "${YELLOW}Python package manager (pip) is missing.${NC}"
    MISSING_PACKAGES+=("python3-pip")
else
    echo -e "${GREEN}Python Package Manager (pip) is ready!${NC}"
fi

# Check venv
if ! python3 -c "import venv" &> /dev/null; then
    echo -e "${YELLOW}Python virtual environment module (venv) is missing.${NC}"
    MISSING_PACKAGES+=("python3-venv")
else
    echo -e "${GREEN}Virtual Environment framework (venv) is ready!${NC}"
fi

# Check Tkinter
if ! python3 -c "import tkinter" &> /dev/null; then
    echo -e "${YELLOW}Tkinter (required for GUI simulation UI) is missing.${NC}"
    MISSING_PACKAGES+=("python3-tk")
else
    echo -e "${GREEN}Graphics Engine engine (Tkinter) is ready!${NC}"
fi

# 3. BULK INSTALL MISSING SUBSYSTEMS
if [ ${#MISSING_PACKAGES[@]} -gt 0 ]; then
    echo -e "\n${YELLOW}The following system modules need to be installed: ${MISSING_PACKAGES[*]}${NC}"
    read -p "Allow installer to fetch them via apt? (y/n): " install_deps
    if [[ "$install_deps" =~ ^[Yy]$ ]]; then
        echo -e "${LIGHT_BLUE}Syncing system repositories and installing dependencies...${NC}"
        sudo apt update && sudo apt install "${MISSING_PACKAGES[@]}" -y
        echo -e "${GREEN}All system modules installed successfully!${NC}"
    else
        echo -e "${RED}Skipping subsystem installation. Setup may fail if dependencies are missing.${NC}"
    fi
else
    echo -e "${GREEN}Perfect! Your Linux system has all core Python components pre-installed.${NC}"
fi

# Exit immediately if any actual file processing step crashes from here
set -e

# 4. SMART VIRTUAL ENVIRONMENT PROVISIONING
echo -e "\n${YELLOW}[3/5] Setting Up Local Project Sandbox...${NC}"
if [ -d ".venv" ]; then
    echo -e "${GREEN}Existing virtual environment (.venv) detected!${NC}"
    read -p "Replace current virtual environment with new environment? [Y/n]" rep_env
    if [[ "$rep_env" =~ ^[Yy]$ ]]; then
        echo -e "${GREEN}Building a new virtual environment (.venv)...${NC}"
        python3 -m venv .venv
        echo -e "${GREEN}Sandbox built successfully!${NC}"
    else
        echo -e "${GREEN}Keeping current virtual environment!${NC}"
    fi
else
    echo -e "${YELLOW}Building virtual environment (.venv)...${NC}"
    python3 -m venv .venv
    echo -e "${GREEN}Sandbox built successfully!${NC}"
fi

# 5. ATTACH ENVIRONMENT AND SYNC PIP PACKAGES
echo -e "\n${YELLOW}[4/5] Syncing Local Application Libraries...${NC}"
source .venv/bin/activate

echo -e "${YELLOW}Checking Python packages...${NC}"
# Run pip installation cleanly (upgrade pip, then sync requirements)
pip install --upgrade pip --quiet
pip install -r requirements.txt --quiet
echo -e "${GREEN}Local library manifest synced and up-to-date!${NC}"

# 6. RE-RUN SATISFACTION SUMMARY
echo -e "\n${GREEN}==================================================${NC}"
echo -e "${GREEN}  Setup Completed! :)${NC}"
echo -e "${GREEN}==================================================${NC}\n"
echo -e "${LIGHT_BLUE}To enter your simulation dashboard, run:${NC}"
echo -e "  ${YELLOW}source .venv/bin/activate${NC}"
echo -e "  ${YELLOW}task run${NC}"