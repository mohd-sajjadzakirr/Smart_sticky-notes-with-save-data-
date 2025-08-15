Write-Host "Starting Sticky Notes App..." -ForegroundColor Green
try {
    python3 sticky_notes.py
} catch {
    Write-Host "Error: Could not start the app. Make sure Python is installed and in your PATH." -ForegroundColor Red
    Write-Host "You can also try running: python3 sticky_notes.py" -ForegroundColor Yellow
}
Read-Host "Press Enter to exit"
