@echo off
cd /d "%~dp0"

REM Run the .pyw file which doesn't show console
pythonw run_no_console.pyw

REM If pythonw fails, try with python but minimize
if errorlevel 1 (
    start /min python run_no_console.pyw
) 