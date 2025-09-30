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

# Prefer pythonw for silent operation (no console window)
if ($pythonPath -eq "python") {
    # Try to find pythonw instead
    try {
        $null = Get-Command "pythonw" -ErrorAction SilentlyContinue
        if ($?) {
            $pythonPath = "pythonw"
        }
    } catch {}
}

Write-Host "Using Python: $pythonPath" -ForegroundColor Green

# Create launcher batch file (silent operation for startup)
$launcher = "@echo off`ncd /d `"%~dp0`"`n$pythonPath Insprash.py"
Set-Content -Path "LaunchInsprash.bat" -Value $launcher
Write-Host "Created LaunchInsprash.bat" -ForegroundColor Green

# Create test launcher with pause for manual testing
$testLauncher = "@echo off`ncd /d `"%~dp0`"`n$pythonPath Insprash.py`necho.`necho Insprash finished. Press any key to close...`npause >nul"
Set-Content -Path "TestInsprash.bat" -Value $testLauncher
Write-Host "Created TestInsprash.bat for manual testing" -ForegroundColor Green

# Test the application manually
Write-Host "`nTesting the application..." -ForegroundColor Yellow
$testChoice = Read-Host "Would you like to test Insprash now? (y/n)"
if ($testChoice -eq "y" -or $testChoice -eq "Y") {
    try {
        Start-Process -FilePath "TestInsprash.bat" -Wait
        Write-Host "Test completed" -ForegroundColor Green
    } catch {
        Write-Host "Test failed: $($_.Exception.Message)" -ForegroundColor Yellow
    }
}

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
Write-Host "Files created:" -ForegroundColor Cyan
Write-Host "  - LaunchInsprash.bat (silent startup version)" -ForegroundColor White
Write-Host "  - TestInsprash.bat (testing version with pause)" -ForegroundColor White
Write-Host "`nTo test: Run TestInsprash.bat" -ForegroundColor Cyan
Write-Host "The app will automatically start on login via LaunchInsprash.bat" -ForegroundColor Cyan

# Check for required Python packages
Write-Host "`nIMPORTANT: Make sure you have the required Python packages installed:" -ForegroundColor Yellow
Write-Host "pip install pillow google-generativeai" -ForegroundColor White

pause