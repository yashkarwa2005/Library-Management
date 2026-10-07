@echo off
TITLE Library Management System - ITL Lab Demonstration
CLS

echo ===============================================================================
echo     LIBRARY MANAGEMENT SYSTEM - ITL LAB & AM PBL DEMONSTRATION
echo     Student Name: Annika Jha ^| Branch: CSE / IT (Sem-5)
echo ===============================================================================
echo.
echo [1] Start Web Dashboard Server (http://127.0.0.1:5000)
echo [2] Run 30-Second Automated Viva Demonstration (--demo)
echo [3] Execute 16-Case Automated Test Suite (--test)
echo [4] Display Terminal ASCII Kanban Board
echo [5] Exit
echo.

set /p choice="Select an option [1-5]: "

if "%choice%"=="1" (
    echo Launching Web Dashboard on http://127.0.0.1:5000...
    start http://127.0.0.1:5000
    python app.py
) else if "%choice%"=="2" (
    echo Running Automated Viva Demonstration...
    python src\main.py --demo
    pause
) else if "%choice%"=="3" (
    echo Running Automated Test Suite...
    python -m unittest discover tests -v
    pause
) else if "%choice%"=="4" (
    echo Rendering Kanban Board...
    python src\main.py --kanban
    pause
) else (
    echo Exiting...
)
