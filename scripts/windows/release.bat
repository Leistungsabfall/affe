@echo off
setlocal enableDelayedExpansion

set "ROOT_DIR=%~dp0\..\.."

cd "%ROOT_DIR%"

:: check_version_string
if "%1"=="" (
    echo.
    echo Usage: release.bat ^<version_string^>
    exit /b 1
)

:: ensure_on_main_branch
echo.
echo Checking if current branch is main...
for /f "delims=" %%a in ('git rev-parse --abbrev-ref HEAD') do set "branch=%%a"
if /i "!branch!" neq "main" (
    echo.
    echo Current branch is '!branch!'
    exit /b 1
)
echo ...OK

:: ensure_no_untracked_files
echo.
echo Checking for untracked files...
set "files="
for /f "delims=" %%a in ('git ls-files --others --exclude-standard') do (
    if not defined files set "files=%%a"
)
if defined files (
    echo.
    echo =====
    git status
    echo =====
    echo.
    echo Found some untracked files
    exit /b 1
)
echo ...OK

:: ensure_no_uncommitted_changes
echo.
echo Checking for uncommitted changes...
git diff-index --quiet HEAD --
if errorlevel 1 (
    echo.
    echo =====
    git status
    echo =====
    echo.
    echo Found some uncommitted changes
    exit /b 1
)
echo ...OK

:: ensure_no_unpushed_commits
echo.
echo Checking for unpushed commits...
set "local_commit_id="
for /f "delims=" %%a in ('git rev-parse HEAD') do set "local_commit_id=%%a"

set "remote_commit_id="
for /f "delims=" %%a in ('git rev-parse origin/main') do set "remote_commit_id=%%a"

if not "!local_commit_id!" == "!remote_commit_id!" (
    echo.
    echo =====
    git status
    echo =====
    echo.
    echo Found unpushed commit(s^)
    exit /b 1
)
echo ...OK

:: check_git_tag
echo.
echo Checking if current commit is tagged...
set "git_tag="
for /f "delims=" %%a in ('git describe --tags --exact-match HEAD') do set "git_tag=%%a"

if defined git_tag (
    echo.
    echo Current commit is already tagged with tag '%git_tag%'.
    exit /b 1
)
echo ...OK

:: test_and_build
echo.
set "VERSION_STRING=%1"
call "%ROOT_DIR%\scripts\windows\build.bat"
if errorlevel 1 (
    exit /b 1
)

endlocal
