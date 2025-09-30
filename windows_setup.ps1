#This script sets up Insprash for Windows systems.

Write-Host "Insprash Windows Setup" -ForegroundColor Cyan
Write-Host "======================" -ForegroundColor Cyan

# Check if Python is installed
Write-Host "Checking for Python installation..." -ForegroundColor Yellow
$pythonPath = ""
$pythonPaths = @("pythonw", "python", "$env:LOCALAPPDATA\Programs\Python\Python*\pythonw.exe", "$env:PROGRAMFILES\Python*\pythonw.exe")

foreach ($path in $pythonPaths) {
    try {
        if ($path -like "*\*") {
            $resolved = Get-ChildItem $path -ErrorAction SilentlyContinue | Select-Object -First 1
            if ($resolved) {
                $pythonPath = "`"$($resolved.FullName)`""
                break
            }
        } else {
            $null = Get-Command $path -ErrorAction SilentlyContinue
            if ($?) {
                $pythonPath = $path
                break
            }
        }
    } catch {
        continue
    }
}

if (-not $pythonPath) {
    Write-Host "ERROR: Python not found. Please install Python from https://python.org" -ForegroundColor Red
    Write-Host "Make sure to check 'Add Python to PATH' during installation." -ForegroundColor Yellow
    pause
    exit 1
}

Write-Host "Found Python: $pythonPath" -ForegroundColor Green

# Check if required files exist
$requiredFiles = @("Insprash.py", "fallback_lines", "gradient_colors", "prompt", "font.ttf")
foreach ($file in $requiredFiles) {
    if (-not (Test-Path $file)) {
        Write-Host "ERROR: Required file '$file' not found in current directory" -ForegroundColor Red
        pause
        exit 1
    }
}

Write-Host "All required files found" -ForegroundColor Green

Write-Host "`nGenerate a Gemini API Key at https://aistudio.google.com/apikey"
$key = Read-Host "Paste Gemini API Key (Leave blank to skip Gemini)"
if (-not $key) {
    $key = "none"
}
Set-Content -Path "gemini_api_key" -Value $key
Write-Host "API Key saved" -ForegroundColor Green

$launcher = "@echo off`ncd /d `"%~dp0`"`n$pythonPath Insprash.py`npause"
Set-Content -Path "LaunchInsprash.bat" -Value $launcher
Write-Host "Created LaunchInsprash.bat" -ForegroundColor Green

# Test the batch file
Write-Host "`nTesting the launcher..." -ForegroundColor Yellow
try {
    $testResult = & ".\LaunchInsprash.bat"
    Write-Host "Launcher test completed" -ForegroundColor Green
} catch {
    Write-Host "WARNING: Launcher test failed: $($_.Exception.Message)" -ForegroundColor Yellow
}

# Ensure startup folder exists
$startupFolder = "$env:APPDATA\Microsoft\Windows\Start Menu\Programs\Startup"
if (-not (Test-Path $startupFolder)) {
    Write-Host "ERROR: Startup folder not found at $startupFolder" -ForegroundColor Red
    Write-Host "Manual step: Copy LaunchInsprash.bat to your startup folder" -ForegroundColor Yellow
} else {
    $startup = "$startupFolder\LaunchInsprash.bat"
    try {
        Copy-Item -Path "LaunchInsprash.bat" -Destination $startup -Force
        Write-Host "Added Insprash to startup folder: $startup" -ForegroundColor Green
    } catch {
        Write-Host "ERROR: Failed to copy to startup folder. Run as Administrator if needed." -ForegroundColor Red
        Write-Host "Manual step: Copy LaunchInsprash.bat to $startupFolder" -ForegroundColor Yellow
    }
}

Write-Host "`nSetup complete!" -ForegroundColor Green
Write-Host "You can test by running: .\LaunchInsprash.bat" -ForegroundColor Cyan
Write-Host "Or log out and back in to test automatic startup." -ForegroundColor Cyan

# Check for required Python packages
Write-Host "`nIMPORTANT: Make sure you have the required Python packages installed:" -ForegroundColor Yellow
Write-Host "pip install pillow google-generativeai requests" -ForegroundColor White

pause