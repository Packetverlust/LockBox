$ErrorActionPreference = "Stop"

$repo = "packetverlust/lockbox"
$installDir = "$env:LOCALAPPDATA\LockBox"
$exe = "$installDir\lockbox.exe"

Write-Host ""
Write-Host "  LockBox Installer" -ForegroundColor Cyan
Write-Host "  ─────────────────" -ForegroundColor DarkGray
Write-Host ""

Write-Host "  Fetching latest release..." -ForegroundColor Gray
$release = Invoke-RestMethod -Uri "https://api.github.com/repos/$repo/releases/latest"
$version = $release.tag_name
$asset = $release.assets | Where-Object { $_.name -like "*windows*" -or $_.name -like "*.exe" } | Select-Object -First 1

if (-not $asset) {
    Write-Host "  [ERROR] No Windows binary found in release $version" -ForegroundColor Red
    exit 1
}

Write-Host "  Latest version: $version" -ForegroundColor Green

if (-not (Test-Path $installDir)) {
    New-Item -ItemType Directory -Path $installDir | Out-Null
}

$tmpFile = "$env:TEMP\lockbox_setup.exe"
Write-Host "  Downloading $($asset.name)..." -ForegroundColor Gray
Invoke-WebRequest -Uri $asset.browser_download_url -OutFile $tmpFile -UseBasicParsing

Copy-Item -Path $tmpFile -Destination $exe -Force
Remove-Item $tmpFile -Force

$userPath = [Environment]::GetEnvironmentVariable("PATH", "User")
if ($userPath -notlike "*$installDir*") {
    [Environment]::SetEnvironmentVariable("PATH", "$userPath;$installDir", "User")
    Write-Host "  Added to PATH" -ForegroundColor Gray
}

Write-Host ""
Write-Host "  LockBox $version installed successfully." -ForegroundColor Green
Write-Host "  Restart your terminal, then run: lockbox --help" -ForegroundColor Cyan
Write-Host ""
