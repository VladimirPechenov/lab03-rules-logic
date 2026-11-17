@echo off
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" py -3 -m venv .venv
.venv\Scripts\python.exe -m pip install -e "./python[dev,report]"
if errorlevel 1 goto failed
.venv\Scripts\python.exe -m ruff check python
if errorlevel 1 goto failed
.venv\Scripts\python.exe -m pytest python\tests
if errorlevel 1 goto failed
.venv\Scripts\python.exe -m rules.scenarios
if errorlevel 1 goto failed
pause
exit /b 0
:failed
pause
exit /b 1
