$ErrorActionPreference = "Stop"

$AppName = "myapp"
$MainFile = "main.py"
$TargetDir = "$HOME\AppData\Local\Programs\PythonApps"
$VenvPath = ".\.venv"

# Create virtual environment
python -m venv $VenvPath

# Install dependencies
& "$VenvPath\Scripts\pip.exe" install -r requirements.txt
& "$VenvPath\Scripts\pip.exe" install pyinstaller

# Build standalone executable
& "$VenvPath\Scripts\pyinstaller.exe" --onefile --name $AppName $MainFile

# Create target directory
if (-not (Test-Path $TargetDir)) {
    New-Item -ItemType Directory -Path $TargetDir | Out-Null
}

# Copy executable to target
Copy-Item "dist\$AppName.exe" -Destination "$TargetDir\$AppName.exe" -Force

# PATH check
$EnvPath = [System.Environment]::GetEnvironmentVariable("Path", "User")
if ($EnvPath -notlike "*$($TargetDir)*") {
    Write-Warning "`n⚠️ $TargetDir is not in your PATH."
    Write-Host "👉 Add it with this command:"
    Write-Host "`$env:Path += ';$TargetDir'"
    Write-Host "Or permanently using:"
    Write-Host "[Environment]::SetEnvironmentVariable('Path', `"$EnvPath;$TargetDir`", 'User')"
}

# Cleanup
Remove-Item -Recurse -Force build, dist, "__pycache__", "$AppName.spec"

# Done
Write-Host "`n✅ Installed $AppName.exe to $TargetDir"
Write-Host "You can now run: $AppName"
