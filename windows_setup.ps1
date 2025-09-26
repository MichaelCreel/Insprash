#This script sets up Insprash for Windows systems.

Write-Host "Generate a Gemini API Key at https://aistudio.google.com/apikey"
$key = Read-Host "Paste Gemini API Key: (Leave blank to skip Gemini) "
Set-Content -Path "gemini_api_key" -Value $key
Write-Host "API Key Written"

$launcher = "@echo off`ncd /d `"%~dp0`"`npythonw Insprash.py"
Set-Content -Path "LaunchInsprash.bat" -Value $launcher
Write-Host "Created LaunchInsprash.bat"

$startup = "$env:APPDATA\Microsoft\Windows\Start Menu\Programs\Startup\LaunchInsprash.bat"
Copy-Item -Path "LaunchInsprash.bat" -Destination $startup -Force
Write-Host "Added Insprash to startup folder"

Write-Host "Setup complete. Insprash should now run on user login."