# mytop

Lightweight Linux TUI task manager built in Python, that alows to kill processes.

## Dependencies
* **Python 3.10+**
* **psutil** 
* **curses** (Built-in)
* **PyInstaller** (For binary compilation)

## Controls
* `▲ / ▼`: Navigate process list
* `K` / `k`: Kill selected process
* `Q` / `q`: Quit

## Example
<img width="2560" height="1440" alt="image" src="https://github.com/user-attachments/assets/d38ac134-32f7-472f-b862-2ad0d720cf02" />



## Installation

## Run from Source
```bash
pip install psutil
python main.py

Install Globally as System Binary
Bash

# 1. Build environment
python -m venv venv
source venv/bin/activate.fish
pip install psutil pyinstaller

# 2. Compile
pyinstaller --onefile --name mytop main.py

# 3. Move to system PATH
sudo cp dist/mytop /usr/bin/mytop
sudo chmod +x /usr/bin/mytop
```

### Usage
```bash
mytop
```
