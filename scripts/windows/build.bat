@echo off
setlocal

set "APP_NAME=affe.exe"
set "ROOT_DIR=%~dp0\..\.."
set "TMP_README_MODULE=src\tmp_readme_module.py"
set "TMP_CHANGELOG_MODULE=src\tmp_changelog_module.py"
set "TMP_LICENSE_MODULE=src\tmp_license_module.py"
set "TMP_THIRD_PARTY_LICENSES_MODULE=src\tmp_third_party_licenses_module.py"
set "TMP_VERSION_MODULE=src\tmp_version_module.py"
set "VENV_PYTHON_EXE=%ROOT_DIR%\venv\Scripts\python.exe"

cd %ROOT_DIR%

:: ensure_venv_exists
if not exist "%ROOT_DIR%\venv" (
    cmd /c "echo venv\ dir is missing. Please run .\setup.bat first"
    exit /b 1
)

echo Using virtual environment Python: "%VENV_PYTHON_EXE%"
if not exist "%VENV_PYTHON_EXE%" (
    echo Error: Virtual environment Python executable not found at "%VENV_PYTHON_EXE%"
    exit /b 1
)

:: run_tests
echo Running unit tests:
"%VENV_PYTHON_EXE%" -m unittest discover "%ROOT_DIR%\test" -f
if errorlevel 1 (
    echo.
    echo All tests have to pass. Aborting.
    exit /b 1
)
echo.

:: create_readme_info
echo Creating README information...
(
    echo readme = r'''
    type "README.md"
    echo '''
) > "%TMP_README_MODULE%.tmp"
move /y "%TMP_README_MODULE%.tmp" "%TMP_README_MODULE%" > nul
if errorlevel 1 (
    echo Error creating README module.
    exit /b 1
)

:: create_changelog_info
echo Creating CHANGELOG information...
(
    echo changelog = r'''
    type "CHANGELOG.md"
    echo '''
) > "%TMP_CHANGELOG_MODULE%.tmp"
move /y "%TMP_CHANGELOG_MODULE%.tmp" "%TMP_CHANGELOG_MODULE%" > nul
if errorlevel 1 (
    echo Error creating CHANGELOG module.
    exit /b 1
)

:: create_license_info
echo Creating LICENSE information...
(
    echo license = r'''
    type "LICENSE"
    echo '''
) > "%TMP_LICENSE_MODULE%.tmp"
move /y "%TMP_LICENSE_MODULE%.tmp" "%TMP_LICENSE_MODULE%" > nul
if errorlevel 1 (
    echo Error creating CHANGELOG module.
    exit /b 1
)

:: create_third_party_licenses_info
echo Creating third-party-licenses information...
(
    echo third_party_licenses = r'''
    type "third-party-licenses.txt"
    echo '''
) > "%TMP_THIRD_PARTY_LICENSES_MODULE%.tmp"
move /y "%TMP_THIRD_PARTY_LICENSES_MODULE%.tmp" "%TMP_THIRD_PARTY_LICENSES_MODULE%" > nul
if errorlevel 1 (
    echo Error creating third-party-licenses module.
    exit /b 1
)

:: create_version_info
echo Creating version information...
if defined VERSION_STRING (
    set "version=%VERSION_STRING%"
) else (
    set "version=dev"
)
echo version = '%version%' > "%TMP_VERSION_MODULE%"
if errorlevel 1 (
    echo Error creating version module.
    exit /b 1
)

::freeze_app
echo Building application:
set "PYTHONOPTIMIZE=2"
"%VENV_PYTHON_EXE%" -m PyInstaller --distpath "." --paths=python-prompt-toolkit --onefile --name "%APP_NAME%" --icon res\icon.ico src\main.py
if errorlevel 1 (
    echo PyInstaller failed.
    exit /b 1
)
move /y affe.exe bin\affe.exe
echo.

::cleanup
echo Cleaning up build artifacts...
if exist "build" rmdir /s /q "build"
if exist "%APP_NAME%.spec" del "%APP_NAME%.spec"
if exist "%TMP_README_MODULE%" del "%TMP_README_MODULE%"
if exist "%TMP_CHANGELOG_MODULE%" del "%TMP_CHANGELOG_MODULE%"
if exist "%TMP_LICENSE_MODULE%" del "%TMP_LICENSE_MODULE%"
if exist "%TMP_THIRD_PARTY_LICENSES_MODULE%" del "%TMP_THIRD_PARTY_LICENSES_MODULE%"
if exist "%TMP_VERSION_MODULE%" del "%TMP_VERSION_MODULE%"

echo Build finished
endlocal
