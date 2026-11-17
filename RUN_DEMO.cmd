@echo off
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
  py -3 -m venv .venv
  if errorlevel 1 goto failed
  .venv\Scripts\python.exe -m pip install -e "./python[dev,report]"
  if errorlevel 1 goto failed
)
.venv\Scripts\python.exe -c "import rules" >nul 2>&1
if errorlevel 1 .venv\Scripts\python.exe -m pip install -e .\python
.venv\Scripts\python.exe -m rules.demo
if errorlevel 1 goto failed
exit /b 0
:failed
pause
exit /b 1
