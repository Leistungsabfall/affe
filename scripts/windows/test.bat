@echo off
setlocal

set "ROOT_DIR=%~dp0\..\.."
set "VENV_PYTHON_EXE=%ROOT_DIR%\venv\Scripts\python.exe"

cd %ROOT_DIR%

%VENV_PYTHON_EXE% -m coverage run ^
--source=handlers.keys,util.text_helper,util.lexer_helper ^
-m unittest discover %ROOT_DIR%/test
if errorlevel 1 (
    echo.
    exit /b 1
)

echo.
%VENV_PYTHON_EXE% -m coverage report -m
del .coverage
