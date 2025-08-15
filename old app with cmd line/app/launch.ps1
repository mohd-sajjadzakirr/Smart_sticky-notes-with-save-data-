# Smart Notes Widget Launcher
Write-Host "🚀 Starting Smart Notes Widget..." -ForegroundColor Green

try {
    # Change to script directory
    Set-Location $PSScriptRoot
    
    # Check if Python is available
    if (Get-Command python -ErrorAction SilentlyContinue) {
        python main.py
    } elseif (Get-Command python3 -ErrorAction SilentlyContinue) {
        python3 main.py
    } else {
        Write-Host "❌ Error: Python is not installed or not in PATH" -ForegroundColor Red
        Write-Host "Please install Python 3.6+ and try again" -ForegroundColor Yellow
        Read-Host "Press Enter to exit"
        exit 1
    }
} catch {
    Write-Host "❌ Error: Could not start Smart Notes Widget" -ForegroundColor Red
    Write-Host "Error details: $($_.Exception.Message)" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
} 