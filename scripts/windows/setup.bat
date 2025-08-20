@echo off
setlocal

set "ROOT_DIR=%~dp0\..\.."
set "PYTHON_PATH=%USERPROFILE%\AppData\Local\Programs\Python\Python38\python.exe"

:: Check for python 3.8
echo.
echo Checking if Python 3.8 is installed...

if not exist %PYTHON_PATH% (
    %ROOT_DIR%\setup\python-3.8.20-amd64-full.exe
)

:: create_virtualenv
echo.
echo Creating virtual environment...
%PYTHON_PATH% -m venv "%ROOT_DIR%\venv"
if %ERRORLEVEL% NEQ 0 (
    echo Error creating virtual environment. Ensure Python 3.8 is installed.
    exit /b 1
)

:: activate_virtualenv
echo.
echo Activating virtual environment...
set "ACTIVATE_PATH=%ROOT_DIR%\venv\Scripts\activate.bat"
if exist %ACTIVATE_PATH% (
    call %ACTIVATE_PATH%
    echo Virtual environment activated.
) else (
    echo Virtual environment activation script not found. Checked %ACTIVATE_PATH%
    exit /b 1
)

:: upgrade_pip
echo.
echo Upgrading pip...
set "VENV_PYTHON=%ROOT_DIR%\venv\Scripts\python.exe"
%VENV_PYTHON% -m pip install --upgrade pip
if %ERRORLEVEL% NEQ 0 (
    echo Error upgrading pip.
    exit /b 1
)

:: install_env_dependencies
echo.
echo Installing Python dependencies from requirements.txt...
%VENV_PYTHON% -m pip install --upgrade -r "%ROOT_DIR%\requirements.txt"
if %ERRORLEVEL% NEQ 0 (
    echo Error installing Python dependencies.
    exit /b 1
)

endlocal
