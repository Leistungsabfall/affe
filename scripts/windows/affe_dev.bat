@echo off
setlocal

set "ROOT_DIR=%~dp0\..\.."
set "VENV_PYTHON_EXE=%ROOT_DIR%\venv\Scripts\python.exe"
set "PYTHONPATH=%PYTHONPATH%;%ROOT_DIR%\python-prompt-toolkit"

"%VENV_PYTHON_EXE%" %ROOT_DIR%\src\main.py %*

endlocal
