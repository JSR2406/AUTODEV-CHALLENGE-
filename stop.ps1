# AutoDev Platform - Stop Script
# PowerShell version for Windows

Write-Host "🛑 Stopping AutoDev Platform..." -ForegroundColor Yellow
Write-Host ""

# Kill Python processes
Write-Host "Stopping agent processes..." -ForegroundColor Yellow
Get-Process python -ErrorAction SilentlyContinue | Where-Object { $_.Path -like "*agent*" } | Stop-Process -Force
Get-Process python -ErrorAction SilentlyContinue | Stop-Process -Force
Write-Host "✅ Stopped all agent processes" -ForegroundColor Green

# Stop Docker services
Write-Host "Stopping Docker services..." -ForegroundColor Yellow
docker-compose down
Write-Host "✅ Stopped Docker services" -ForegroundColor Green

# Kill Node processes (dashboard)
Write-Host "Stopping dashboard..." -ForegroundColor Yellow
Get-Process node -ErrorAction SilentlyContinue | Stop-Process -Force
Write-Host "✅ Stopped dashboard" -ForegroundColor Green

Write-Host ""
Write-Host "✅ AutoDev Platform stopped successfully" -ForegroundColor Green
