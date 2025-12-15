# Create desktop shortcut for AetherMUD LLM Assistant

$WshShell = New-Object -ComObject WScript.Shell
$DesktopPath = [Environment]::GetFolderPath("Desktop")
$ShortcutPath = Join-Path $DesktopPath "AetherMUD Assistant.lnk"
$TargetPath = "pythonw.exe"  # pythonw = no console window
$Arguments = "`"$PSScriptRoot\launch_assistant_gui.pyw`""
$WorkingDir = $PSScriptRoot
$IconPath = Join-Path $PSScriptRoot "assets\favicon_io-AetherMUD\favicon.ico"

Write-Host "Clearing Windows icon cache..." -ForegroundColor Yellow
# Kill explorer to clear icon cache
Stop-Process -Name explorer -Force -ErrorAction SilentlyContinue

# Clear icon cache files
$CacheLocations = @(
    "$env:LOCALAPPDATA\IconCache.db",
    "$env:LOCALAPPDATA\Microsoft\Windows\Explorer\iconcache_*.db"
)

foreach ($CacheFile in $CacheLocations) {
    if (Test-Path $CacheFile) {
        Remove-Item $CacheFile -Force -ErrorAction SilentlyContinue
        Write-Host "Cleared: $CacheFile" -ForegroundColor Yellow
    }
}

# Remove old shortcut if it exists
if (Test-Path $ShortcutPath) {
    Remove-Item $ShortcutPath -Force
    Write-Host "Removed old shortcut" -ForegroundColor Yellow
}

$Shortcut = $WshShell.CreateShortcut($ShortcutPath)
$Shortcut.TargetPath = $TargetPath
$Shortcut.Arguments = $Arguments
$Shortcut.WorkingDirectory = $WorkingDir
$Shortcut.IconLocation = $IconPath
$Shortcut.Description = "AetherMUD LLM Assistant"
$Shortcut.Save()

Write-Host "✅ Desktop shortcut created: $ShortcutPath" -ForegroundColor Green
Write-Host "Icon path: $IconPath" -ForegroundColor Cyan

# Restart explorer
Start-Process explorer.exe
Start-Sleep -Seconds 2

Write-Host "✅ Icon cache cleared and explorer restarted" -ForegroundColor Green
Write-Host "Double-click 'AetherMUD Assistant' on your desktop to launch!" -ForegroundColor Cyan
