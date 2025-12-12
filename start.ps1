# AutoDev Platform - Complete Startup Script
# PowerShell version for Windows

Write-Host "🚀 AutoDev Platform - Complete Startup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check prerequisites
Write-Host "📋 Checking prerequisites..." -ForegroundColor Yellow

if (!(Get-Command docker -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Docker not found. Please install Docker Desktop first." -ForegroundColor Red
    exit 1
}

if (!(Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Python not found. Please install Python 3.11+" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Prerequisites OK" -ForegroundColor Green
Write-Host ""

# Start infrastructure
Write-Host "🐳 Starting infrastructure (PostgreSQL, Redis, RabbitMQ)..." -ForegroundColor Yellow
docker-compose up -d postgres redis rabbitmq

Write-Host "⏳ Waiting for services to be ready (30 seconds)..." -ForegroundColor Yellow
Start-Sleep -Seconds 30

# Check database
Write-Host "🔍 Checking database connection..." -ForegroundColor Yellow
$dbCheck = docker exec autodev-postgres pg_isready -U postgres 2>$null
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Database ready" -ForegroundColor Green
} else {
    Write-Host "❌ Database not ready" -ForegroundColor Red
}

# Check Redis
Write-Host "🔍 Checking Redis connection..." -ForegroundColor Yellow
$redisCheck = docker exec autodev-redis redis-cli -a autodev_redis_2025 ping 2>$null
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Redis ready" -ForegroundColor Green
} else {
    Write-Host "❌ Redis not ready" -ForegroundColor Red
}

Write-Host ""

# Install Python dependencies
Write-Host "📦 Installing Python dependencies..." -ForegroundColor Yellow
Set-Location agents
pip install -q -r requirements.txt
Set-Location ..

Write-Host "✅ Dependencies installed" -ForegroundColor Green
Write-Host ""

# Create logs directory
if (!(Test-Path "logs")) {
    New-Item -ItemType Directory -Path "logs" | Out-Null
}

# Start agents
Write-Host "🤖 Starting AI agents..." -ForegroundColor Yellow

Start-Process python -ArgumentList "agents/planning_agent.py" -RedirectStandardOutput "logs/planning.log" -RedirectStandardError "logs/planning_error.log" -WindowStyle Hidden
Write-Host "✅ Planning Agent started" -ForegroundColor Green

Start-Process python -ArgumentList "agents/frontend_agent.py" -RedirectStandardOutput "logs/frontend.log" -RedirectStandardError "logs/frontend_error.log" -WindowStyle Hidden
Write-Host "✅ Frontend Agent started" -ForegroundColor Green

Start-Process python -ArgumentList "agents/backend_agent.py" -RedirectStandardOutput "logs/backend.log" -RedirectStandardError "logs/backend_error.log" -WindowStyle Hidden
Write-Host "✅ Backend Agent started" -ForegroundColor Green

Start-Process python -ArgumentList "agents/database_agent.py" -RedirectStandardOutput "logs/database.log" -RedirectStandardError "logs/database_error.log" -WindowStyle Hidden
Write-Host "✅ Database Agent started" -ForegroundColor Green

Start-Process python -ArgumentList "agents/testing_agent.py" -RedirectStandardOutput "logs/testing.log" -RedirectStandardError "logs/testing_error.log" -WindowStyle Hidden
Write-Host "✅ Testing Agent started" -ForegroundColor Green

Write-Host ""
Write-Host "⏳ Waiting for agents to initialize (10 seconds)..." -ForegroundColor Yellow
Start-Sleep -Seconds 10

# Check agent health
Write-Host ""
Write-Host "🏥 Checking agent health..." -ForegroundColor Yellow

function Test-AgentHealth {
    param($Port, $Name)
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:$Port/health" -TimeoutSec 2 -UseBasicParsing
        if ($response.StatusCode -eq 200) {
            Write-Host "✅ $Name Agent: Healthy" -ForegroundColor Green
            return $true
        }
    } catch {
        Write-Host "❌ $Name Agent: Not responding" -ForegroundColor Red
        return $false
    }
}

Test-AgentHealth 8000 "Planning"
Test-AgentHealth 8001 "Frontend"
Test-AgentHealth 8002 "Backend"
Test-AgentHealth 8003 "Database"
Test-AgentHealth 8004 "Testing"

Write-Host ""

# Start dashboard
Write-Host "📊 Starting monitoring dashboard..." -ForegroundColor Yellow
Set-Location dashboard

if (!(Test-Path "node_modules")) {
    Write-Host "📦 Installing dashboard dependencies (first time only)..." -ForegroundColor Yellow
    npm install 2>&1 | Out-Null
}

Start-Process npm -ArgumentList "start" -RedirectStandardOutput "../logs/dashboard.log" -RedirectStandardError "../logs/dashboard_error.log" -WindowStyle Hidden
Write-Host "✅ Dashboard started" -ForegroundColor Green

Set-Location ..

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "✅ AutoDev Platform is READY!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "📌 Access Points:" -ForegroundColor Yellow
Write-Host ""
Write-Host "  🌐 Monitoring Dashboard:  http://localhost:3000" -ForegroundColor White
Write-Host "  📊 n8n Workflow Engine:   http://localhost:5678" -ForegroundColor White
Write-Host "     (Username: admin, Password: autodev2025)" -ForegroundColor Gray
Write-Host ""
Write-Host "  🤖 Agent API Documentation:" -ForegroundColor White
Write-Host "     Planning Agent:   http://localhost:8000/docs" -ForegroundColor White
Write-Host "     Frontend Agent:   http://localhost:8001/docs" -ForegroundColor White
Write-Host "     Backend Agent:    http://localhost:8002/docs" -ForegroundColor White
Write-Host "     Database Agent:   http://localhost:8003/docs" -ForegroundColor White
Write-Host "     Testing Agent:    http://localhost:8004/docs" -ForegroundColor White
Write-Host ""
Write-Host "  🗄️  Infrastructure:" -ForegroundColor White
Write-Host "     PostgreSQL:       localhost:5432" -ForegroundColor White
Write-Host "     Redis:            localhost:6379" -ForegroundColor White
Write-Host "     RabbitMQ UI:      http://localhost:15672" -ForegroundColor White
Write-Host ""
Write-Host "📝 Quick Test:" -ForegroundColor Yellow
Write-Host "   python orchestrator.py" -ForegroundColor White
Write-Host ""
Write-Host "📋 View Logs:" -ForegroundColor Yellow
Write-Host "   Get-Content logs/planning.log -Tail 20 -Wait" -ForegroundColor White
Write-Host "   docker-compose logs -f postgres" -ForegroundColor White
Write-Host ""
Write-Host "🛑 Stop All:" -ForegroundColor Yellow
Write-Host "   ./stop.ps1" -ForegroundColor White
Write-Host ""
Write-Host "💡 Tip: Open http://localhost:3000 to start processing stories!" -ForegroundColor Cyan
Write-Host ""
