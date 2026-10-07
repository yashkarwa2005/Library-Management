@echo off
TITLE Library Management System - Agile Methodologies PBL
CLS

echo ===============================================================================
echo     LIBRARY MANAGEMENT SYSTEM - SCRUM AGILE METHODOLOGIES PBL
echo     Author / Scrum Lead: Annika Jha
echo ===============================================================================
echo.
echo [1] Launch Web Application (Recommended: http://127.0.0.1:5000)
echo [2] Launch Interactive Terminal Console
echo [3] Run Instant Automated Viva Demonstration (--demo)
echo [4] Display Terminal ASCII Kanban Board (--kanban)
echo [5] Execute Automated Unit and Integration Tests (--test)
echo [6] Exit
echo.

set /p choice="Select an option [1-6]: "

if "%choice%"=="1" (
    echo Launching Web Application...
    python app.py
) else if "%choice%"=="2" (
    echo Launching Interactive Console...
    python src\main.py
) else if "%choice%"=="3" (
    echo Running Viva Demonstration...
    python src\main.py --demo
    pause
) else if "%choice%"=="4" (
    echo Rendering Kanban Board...
    python src\main.py --kanban
    pause
) else if "%choice%"=="5" (
    echo Running Test Suite...
    python -m unittest discover tests -v
    pause
) else (
    echo Exiting...
)
