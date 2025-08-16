# PowerShell script to launch Instance Controller
Write-Host "Launching Instance Controller..." -ForegroundColor Green

# Get the current directory
$currentDir = Get-Location

# Check if the .pyw file exists
if (Test-Path "instance_controller.pyw") {
    Write-Host "Found instance_controller.pyw" -ForegroundColor Yellow
    
    # Launch using pythonw
    try {
        Start-Process -FilePath "pythonw" -ArgumentList "instance_controller.pyw" -WorkingDirectory $currentDir
        Write-Host "Instance Controller launched successfully!" -ForegroundColor Green
    }
    catch {
        Write-Host "Error launching with pythonw: $_" -ForegroundColor Red
        Write-Host "Trying alternative method..." -ForegroundColor Yellow
        
        # Alternative: try direct execution
        try {
            & pythonw instance_controller.pyw
        }
        catch {
            Write-Host "Failed to launch Instance Controller" -ForegroundColor Red
            Write-Host "Press any key to exit..." -ForegroundColor Yellow
            $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
        }
    }
}
else {
    Write-Host "Error: instance_controller.pyw not found!" -ForegroundColor Red
    Write-Host "Current directory: $currentDir" -ForegroundColor Yellow
    Write-Host "Press any key to exit..." -ForegroundColor Yellow
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
} 