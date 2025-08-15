@echo off
cd /d "%~dp0"

REM Try to run with pythonw (no console)
pythonw main.py 2>nul
if errorlevel 1 (
    REM If pythonw fails, try with python but minimize the console
    start /min python main.py
) else (
    REM If pythonw succeeds, the app is running without console
    echo Smart Notes Widget started successfully!
    timeout /t 2 /nobreak >nul
) 