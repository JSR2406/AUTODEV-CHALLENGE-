# AutoDev Platform - Start All Agents Script
# Starts all 5 agents in separate visible windows

Write-Host "Starting AutoDev Platform - All Agents" -ForegroundColor Cyan
Write-Host "=======================================" -ForegroundColor Cyan
Write-Host ""

# Kill any existing Python processes (except current)
Write-Host "Cleaning up existing processes..." -ForegroundColor Yellow
Get-Process python -ErrorAction SilentlyContinue | Where-Object { $_.Id -ne $PID } | Stop-Process -Force -ErrorAction SilentlyContinue
Start-Sleep -Seconds 2

# Start each agent in a new window
Write-Host "Starting agents..." -ForegroundColor Yellow

Write-Host "  Starting Planning Agent (Port 8000)..." -ForegroundColor White
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD\agents'; Write-Host 'Planning Agent Starting...' -ForegroundColor Green; python planning_agent.py"
Start-Sleep -Seconds 3

Write-Host "  Starting Frontend Agent (Port 8001)..." -ForegroundColor White
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD\agents'; Write-Host 'Frontend Agent Starting...' -ForegroundColor Green; python frontend_agent.py"
Start-Sleep -Seconds 2

Write-Host "  Starting Backend Agent (Port 8002)..." -ForegroundColor White
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD\agents'; Write-Host 'Backend Agent Starting...' -ForegroundColor Green; python backend_agent.py"
Start-Sleep -Seconds 2

Write-Host "  Starting Database Agent (Port 8003)..." -ForegroundColor White
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD\agents'; Write-Host 'Database Agent Starting...' -ForegroundColor Green; python database_agent.py"
Start-Sleep -Seconds 2

Write-Host "  Starting Testing Agent (Port 8004)..." -ForegroundColor White
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD\agents'; Write-Host 'Testing Agent Starting...' -ForegroundColor Green; python testing_agent.py"

Write-Host ""
Write-Host "Waiting for agents to initialize (15 seconds)..." -ForegroundColor Yellow
Start-Sleep -Seconds 15

# Check agent health
Write-Host ""
Write-Host "Checking agent health..." -ForegroundColor Yellow
Write-Host ""

$healthyCount = 0
@(
    @(8000, "Planning Agent"),
    @(8001, "Frontend Agent"),
    @(8002, "Backend Agent"),
    @(8003, "Database Agent"),
    @(8004, "Testing Agent")
) | ForEach-Object {
    $port = $_[0]
    $name = $_[1]
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:$port/health" -TimeoutSec 3 -UseBasicParsing
        if ($response.StatusCode -eq 200) {
            Write-Host "  [OK] $name (Port $port): HEALTHY" -ForegroundColor Green
            $script:healthyCount++
        }
        else {
            Write-Host "  [FAIL] $name (Port $port): UNHEALTHY" -ForegroundColor Red
        }
    }
    catch {
        Write-Host "  [FAIL] $name (Port $port): OFFLINE" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "=======================================" -ForegroundColor Cyan
if ($healthyCount -eq 5) {
    Write-Host "SUCCESS: All 5 agents are healthy!" -ForegroundColor Green
}
else {
    Write-Host "WARNING: Only $healthyCount/5 agents are healthy" -ForegroundColor Yellow
    Write-Host "Check the agent windows for error messages" -ForegroundColor Yellow
}
Write-Host "=======================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Dashboard: http://localhost:3001" -ForegroundColor Cyan
Write-Host "Refresh the dashboard to see updated agent status" -ForegroundColor White
Write-Host ""
