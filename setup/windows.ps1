# Custom color helper
function Write-Color ($text, $color) {
    Write-Host $text -ForegroundColor $color
}

Write-Color "Starting Physics-Simulation Installer Wizard...`n" "Cyan"

# DYNAMIC ROOT DETECTION: Forces PowerShell to target the main project folder
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location "$ScriptDir\.."

# 1. CORE PYTHON CHECK
Write-Color "[1/4] Checking Python Installation..." "Yellow"
if (-not (Get-Command "python" -ErrorAction SilentlyContinue)) {
    Write-Color "Python is not installed on this system." "Red"
    Write-Color "Please download and install Python from https://www.python.org/downloads/" "Red"
    Write-Color "Make sure to check the box that says 'Add Python to PATH' during installation." "Yellow"
    Exit 1
} else {
    $pyVersion = python --version
    Write-Color "$pyVersion core is ready!" "Green"
}

# 2. VIRTUAL ENVIRONMENT PROVISIONING
Write-Color "`n[2/4] Setting Up Local Project Sandbox..." "Yellow"
if (Test-Path ".venv") {
    Write-Color "Existing virtual environment (.venv) detected!" "Green"
    $rep_env = Read-Host "Replace current virtual environment with new environment? [Y/n]"
    if ($rep_env -match "^[Yy]$" -or $rep_env -eq "") {
        Write-Color "Building a new virtual environment (.venv)..." "Green"
        Remove-Item -Recurse -Force .venv
        python -m venv .venv
        Write-Color "Sandbox built successfully!" "Green"
    } else {
        Write-Color "Keeping current virtual environment!" "Green"
    }
} else {
    Write-Color "Building virtual environment (.venv)..." "Yellow"
    python -m venv .venv
    Write-Color "Sandbox built successfully!" "Green"
}

# 3. ATTACH ENVIRONMENT AND SYNC PIP PACKAGES
Write-Color "`n[3/4] Syncing Local Application Libraries..." "Yellow"
# Activate the venv natively in PowerShell
& .venv\Scripts\Activate.ps1

Write-Color "Checking Python packages..." "Yellow"
python -m pip install --upgrade pip --quiet
pip install -r requirements.txt --quiet
Write-Color "Local library manifest synced and up-to-date!" "Green"

# 4. SATISFACTION SUMMARY
Write-Color "`n==================================================" "Green"
Write-Color "  Setup Completed! :)" "Green"
Write-Color "==================================================" "Green"
Write-Color "`nTo enter your simulation dashboard, run:" "Cyan"
Write-Color "  .venv\Scripts\Activate.ps1" "Yellow"
Write-Color "  task run" "Yellow"