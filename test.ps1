# AutoDev Platform - Complete Test & Execution Script
# This script tests all components and runs a complete end-to-end workflow

Write-Host "🧪 AutoDev Platform - Complete Testing & Execution" -ForegroundColor Cyan
Write-Host "====================================================" -ForegroundColor Cyan
Write-Host ""

# Test 1: Check Infrastructure
Write-Host "📋 Test 1: Checking Infrastructure..." -ForegroundColor Yellow
$containers = docker ps --format "{{.Names}}"
$requiredContainers = @("autodev-postgres", "autodev-redis")

foreach ($container in $requiredContainers) {
    if ($containers -contains $container) {
        Write-Host "  ✅ $container is running" -ForegroundColor Green
    }
    else {
        Write-Host "  ❌ $container is NOT running" -ForegroundColor Red
    }
}

# Test 2: Check Agent Health
Write-Host ""
Write-Host "📋 Test 2: Checking Agent Health..." -ForegroundColor Yellow

function Test-AgentHealth {
    param($Port, $Name)
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:$Port/health" -TimeoutSec 3 -UseBasicParsing
        if ($response.StatusCode -eq 200) {
            Write-Host "  ✅ $Name Agent (Port $Port): Healthy" -ForegroundColor Green
            return $true
        }
    }
    catch {
        Write-Host "  ❌ $Name Agent (Port $Port): Not responding" -ForegroundColor Red
        return $false
    }
}

$planningHealthy = Test-AgentHealth 8000 "Planning"

# Test 3: Process a Test Story
if ($planningHealthy) {
    Write-Host ""
    Write-Host "📋 Test 3: Processing Test Story..." -ForegroundColor Yellow
    
    $testStory = @{
        story_id            = "TEST-001"
        session_id          = "test_session_$(Get-Date -Format 'yyyyMMddHHmmss')"
        title               = "User Authentication"
        description         = "As a user, I want to log in with email and password"
        acceptance_criteria = @(
            @{id = 1; text = "User can enter credentials"; priority = "must-have" }
            @{id = 2; text = "System validates credentials"; priority = "must-have" }
        )
        tech_hints          = @{
            requires_auth     = $true
            requires_database = $true
            requires_api      = $true
            requires_ui       = $true
            complexity        = "medium"
        }
        project_id          = "test-project"
    }
    
    try {
        $json = $testStory | ConvertTo-Json -Depth 10
        $response = Invoke-WebRequest -Uri "http://localhost:8000/agents/planning" `
            -Method POST `
            -Body $json `
            -ContentType "application/json" `
            -TimeoutSec 30 `
            -UseBasicParsing
        
        if ($response.StatusCode -eq 200) {
            Write-Host "  ✅ Planning Agent successfully processed story" -ForegroundColor Green
            $result = $response.Content | ConvertFrom-Json
            Write-Host "  📊 Generated:" -ForegroundColor Cyan
            Write-Host "     - Tables: $($result.architecture.database.tables.Count)" -ForegroundColor White
            Write-Host "     - Endpoints: $($result.architecture.backend.endpoints.Count)" -ForegroundColor White
            Write-Host "     - Components: $($result.architecture.frontend.components.Count)" -ForegroundColor White
            Write-Host "     - Execution Time: $([math]::Round($result.execution_time_seconds, 2))s" -ForegroundColor White
        }
    }
    catch {
        Write-Host "  ❌ Failed to process story: $_" -ForegroundColor Red
    }
}
else {
    Write-Host ""
    Write-Host "⚠️  Skipping Test 3: Planning Agent not healthy" -ForegroundColor Yellow
}

# Summary
Write-Host ""
Write-Host "====================================================" -ForegroundColor Cyan
Write-Host "✅ Testing Complete!" -ForegroundColor Green
Write-Host "====================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "📌 Next Steps:" -ForegroundColor Yellow
Write-Host "  1. Start remaining agents (frontend, backend, database, testing)" -ForegroundColor White
Write-Host "  2. Run full orchestrator: python orchestrator.py" -ForegroundColor White
Write-Host "  3. Start dashboard: cd dashboard && npm start" -ForegroundColor White
Write-Host ""
