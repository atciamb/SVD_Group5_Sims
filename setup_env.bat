@echo off
echo Creating isolated virtual environment (.venv)...
python -m venv .venv
echo Installing required packages...
.venv\Scripts\python.exe -m pip install --upgrade pip
.venv\Scripts\pip.exe install -r requirements.txt
echo.
echo Setup complete! Restart VS Code or select .venv as your interpreter.
