@echo off
echo Enabling Smart Notes Auto-Start...
echo.

REM Get the current directory
set "CURRENT_DIR=%~dp0"
set "STARTUP_MANAGER=%CURRENT_DIR%startup_manager_hidden.pyw"

REM Check if startup manager exists
if not exist "%STARTUP_MANAGER%" (
    echo Error: Startup manager not found at %STARTUP_MANAGER%
    pause
    exit /b 1
)

REM Enable auto-start using Python (hidden mode)
python "%STARTUP_MANAGER%" --enable-auto-start

if %ERRORLEVEL% EQU 0 (
    echo.
    echo Success: Auto-start has been enabled!
    echo Smart Notes will now automatically restore all instances when you restart your computer.
) else (
    echo.
    echo Error: Failed to enable auto-start.
)

echo.
pause 