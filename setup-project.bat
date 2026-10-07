@echo off
setlocal enabledelayedexpansion

:: ============================================================================
:: ONE-CLICK GITHUB PROJECT & KANBAN SETUP
:: Agile Methodologies (AM) Project-Based Learning (PBL)
:: ============================================================================

title GitHub Scrum Project Setup - One Click

:: Force UTF-8 encoding in Windows command prompt
chcp 65001 >nul

:: Navigate to script directory
cd /d "%~dp0"

echo.
echo ============================================================================
echo   ONE-CLICK GITHUB PROJECT ^& KANBAN SETUP
echo   Agile Methodologies (AM) PBL - Dynamic Setup System
echo ============================================================================
echo.

:: ----------------------------------------------------------------------------
:: 1. CHECK GIT PREREQUISITE
:: ----------------------------------------------------------------------------
echo [*] Checking Git...
where git >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Git is not installed or not found in PATH!
    echo.
    echo Why it is needed:
    echo   Git is required to inspect your repository's remote and track changes.
    echo.
    echo How to install:
    echo   Download and install Git from: https://git-scm.com/
    echo   Or run: winget install --id Git.Git -e --source winget
    echo.
    echo After installing, please restart this script.
    echo.
    pause
    exit /b 1
)
for /f "tokens=*" %%v in ('git --version 2^>nul') do echo     Found: %%v

:: ----------------------------------------------------------------------------
:: 2. CHECK PYTHON PREREQUISITE
:: ----------------------------------------------------------------------------
echo [*] Checking Python...
set "PY_CMD="
where python >nul 2>&1
if %errorlevel% equ 0 (
    set "PY_CMD=python"
) else (
    where py >nul 2>&1
    if %errorlevel% equ 0 (
        set "PY_CMD=py"
    )
)

if "%PY_CMD%"=="" (
    echo [ERROR] Python is not installed or not found in PATH!
    echo.
    echo Why it is needed:
    echo   Python is used to execute the setup engine and run the PBL application.
    echo.
    echo How to install:
    echo   Download Python 3.8+ from: https://www.python.org/downloads/
    echo   Make sure to check "Add Python to PATH" during installation.
    echo   Or run: winget install --id Python.Python.3.13
    echo.
    pause
    exit /b 1
)
for /f "tokens=*" %%v in ('%PY_CMD% --version 2^>nul') do echo     Found: %%v

:: ----------------------------------------------------------------------------
:: 3. CHECK GITHUB CLI (gh) PREREQUISITE
:: ----------------------------------------------------------------------------
echo [*] Checking GitHub CLI (gh)...
where gh >nul 2>&1
if %errorlevel% neq 0 (
    :: Check standard Windows installation directories
    if exist "%ProgramFiles%\GitHub CLI\gh.exe" (
        set "PATH=%ProgramFiles%\GitHub CLI;!PATH!"
    ) else if exist "%ProgramFiles(x86)%\GitHub CLI\gh.exe" (
        set "PATH=%ProgramFiles(x86)%\GitHub CLI;!PATH!"
    ) else if exist "%LOCALAPPDATA%\Programs\GitHub CLI\gh.exe" (
        set "PATH=%LOCALAPPDATA%\Programs\GitHub CLI;!PATH!"
    )
)

where gh >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo [WARNING] GitHub CLI [gh] was not detected in PATH.
    echo.
    echo Why it is needed:
    echo   GitHub CLI allows secure, tokenless authentication with YOUR OWN GitHub account
    echo   and programmatic creation of Labels, Issues, Milestones, and Kanban boards.
    echo.
    echo Would you like to attempt automated installation via Windows Package Manager [winget]?
    set /p "INSTALL_GH=Install GitHub CLI now? [Y/N]: "
    if /i "!INSTALL_GH!"=="Y" (
        echo [*] Installing GitHub CLI via winget...
        winget install --id GitHub.cli --silent --accept-source-agreements --accept-package-agreements
        if exist "%ProgramFiles%\GitHub CLI\gh.exe" (
            set "PATH=%ProgramFiles%\GitHub CLI;!PATH!"
        )
    )
)

:: Re-verify gh
where gh >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo [ERROR] GitHub CLI is required to continue.
    echo Please install it manually from: https://cli.github.com/
    echo After installation completes, reopen this script.
    echo.
    pause
    exit /b 1
)
for /f "tokens=*" %%v in ('gh --version 2^>nul') do (
    echo     Found: %%v
    goto :gh_checked
)
:gh_checked

:: ----------------------------------------------------------------------------
:: 4. CHECK GITHUB AUTHENTICATION
:: ----------------------------------------------------------------------------
if "%~1"=="--check-config" (
    echo [*] Running in configuration check mode...
    %PY_CMD% "%~dp0.github\setup\setup_project.py" %*
    pause
    exit /b %errorlevel%
)

echo [*] Verifying GitHub authentication status...
gh auth status >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo ============================================================================
    echo   AUTHENTICATION REQUIRED: YOUR OWN GITHUB ACCOUNT
    echo ============================================================================
    echo   You are not logged into GitHub CLI.
    echo   You will now be guided through logging into YOUR OWN GitHub account.
    echo.
    echo   NOTE: This setup NEVER uses personal access tokens stored in files.
    echo         Your credentials remain entirely on your own machine.
    echo ============================================================================
    echo.
    gh auth login -w -s repo,project
    echo.
    gh auth status >nul 2>&1
    if !errorlevel! neq 0 (
        echo [ERROR] GitHub authentication was not completed.
        echo Please run 'gh auth login' manually and retry.
        echo.
        pause
        exit /b 1
    )
)

:: ----------------------------------------------------------------------------
:: 5. EXECUTE SETUP ENGINE
:: ----------------------------------------------------------------------------
echo [*] Launching Agile GitHub Project setup engine...
echo.

%PY_CMD% "%~dp0.github\setup\setup_project.py" %*
set SETUP_EXIT_CODE=%errorlevel%

echo.
if %SETUP_EXIT_CODE% equ 0 (
    echo [SUCCESS] GitHub Scrum Setup completed successfully!
) else (
    echo [WARNING] Setup finished with code %SETUP_EXIT_CODE%. Please review messages above.
)
echo.

pause
exit /b %SETUP_EXIT_CODE%
