# Physics-Simulation

Motion due to gravitational and electrostatic forces

## Getting started with the project:

## Quickstart for linux

```bash
chmod +x setup/linux.bash && ./setup/linux.bash
```

Once the script finishes, simply activate the environment and launch the project:

```bash
source .venv/bin/activate
task run
```

## Quickstart for Windows

```powerShell
./setup/windows.ps1
```

Once the script finishes, simply activate the environment and launch the project:

```powerShell
.venv\Scripts\Activate.ps1
task run
```

## Manual Setup

#### Create a new virtual environment.

```bash
python3 -m venv .venv
```

#### Activate the virtual environment

```bash
source .venv/bin/activate
```

#### Install requirements

```bash
pip install -r requirements.txt
```

#### Run script

```bash
task run
```
