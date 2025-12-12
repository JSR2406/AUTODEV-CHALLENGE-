# 🚀 AutoDev Platform - Multi-Agent Software Development System

An intelligent multi-agent platform that automatically generates full-stack applications from user stories using AI-powered agents.

## 🎯 Overview

AutoDev Platform orchestrates specialized AI agents to transform user stories into production-ready code:

- **Planning Agent**: Generates architecture blueprints
- **Database Agent**: Creates SQL schemas and ORM models
- **Backend Agent**: Generates FastAPI endpoints
- **Frontend Agent**: Creates React components
- **Testing Agent**: Generates comprehensive tests

## 📁 Project Structure

```
autodev-platform/
├── agents/                    # AI Agent services
│   ├── planning_agent.py
│   ├── frontend_agent.py
│   ├── backend_agent.py
│   ├── database_agent.py
│   ├── testing_agent.py
│   ├── requirements.txt
│   └── Dockerfile.*
├── workflows/                 # n8n workflow definitions
├── docker-compose.yml         # Infrastructure setup
├── init-db.sql               # Database schema
├── orchestrator.py           # Agent coordinator
├── test_stories.json         # Sample user stories
├── .env                      # Environment configuration
└── README.md
```

## 🚀 Quick Start

### Prerequisites

- Docker Desktop installed and running
- Python 3.11+ (for local testing)
- 8GB+ RAM recommended

### Step 1: Configure Environment

Edit `.env` file with your API keys (optional for basic demo):

```bash
OPENAI_API_KEY=your-key-here
```

### Step 2: Start Infrastructure

```powershell
# Start database, Redis, RabbitMQ
docker-compose up -d postgres redis rabbitmq

# Wait for services to initialize (30 seconds)
Start-Sleep -Seconds 30

# Verify services are running
docker-compose ps
```

### Step 3: Install Python Dependencies

```powershell
cd agents
pip install -r requirements.txt
```

### Step 4: Start Agents (Manual Mode)

Open 5 separate terminals:

**Terminal 1 - Planning Agent:**
```powershell
cd agents
python planning_agent.py
```

**Terminal 2 - Frontend Agent:**
```powershell
cd agents
python frontend_agent.py
```

**Terminal 3 - Backend Agent:**
```powershell
cd agents
python backend_agent.py
```

**Terminal 4 - Database Agent:**
```powershell
cd agents
python database_agent.py
```

**Terminal 5 - Testing Agent:**
```powershell
cd agents
python testing_agent.py
```

### Step 5: Run Demo

In a new terminal:

```powershell
python orchestrator.py
```

You should see output like:

```
🚀 Processing Story: User Authentication
============================================================

📋 Step 1: Planning Agent...
✅ Planning completed in 0.45s

🗄️  Step 2: Database Agent...
✅ Generated 2 database files

⚙️  Step 3: Backend Agent...
✅ Generated 5 backend files

🎨 Step 4: Frontend Agent...
✅ Generated 3 frontend files

🧪 Step 5: Testing Agent...
✅ Tests: 6 total, Coverage: 87.5%

============================================================
✅ Story processing complete!
============================================================
```

## 🔍 Verify Installation

### Check Agent Health

```powershell
# Planning Agent
curl http://localhost:8000/health

# Frontend Agent
curl http://localhost:8001/health

# Backend Agent
curl http://localhost:8002/health

# Database Agent
curl http://localhost:8003/health

# Testing Agent
curl http://localhost:8004/health
```

### Access API Documentation

- Planning Agent: http://localhost:8000/docs
- Frontend Agent: http://localhost:8001/docs
- Backend Agent: http://localhost:8002/docs
- Database Agent: http://localhost:8003/docs
- Testing Agent: http://localhost:8004/docs

### Query Database

```powershell
docker exec -it autodev-postgres psql -U postgres -d autodev_platform

# View execution logs
SELECT story_id, agent_name, status, created_at 
FROM execution_logs 
ORDER BY created_at DESC 
LIMIT 10;
```

### Check Redis Cache

```powershell
docker exec -it autodev-redis redis-cli -a autodev_redis_2025

# List all keys
KEYS *
```

## 📊 Architecture

```
User Story → Planning Agent → Architecture Blueprint
                ↓
    ┌───────────┼───────────┐
    ↓           ↓           ↓
Database    Backend    Frontend
 Agent       Agent       Agent
    ↓           ↓           ↓
    └───────────┼───────────┘
                ↓
         Testing Agent
                ↓
         Generated Code
```

## 🧪 Testing with Custom Stories

Create your own user story:

```python
from orchestrator import SimpleOrchestrator

orchestrator = SimpleOrchestrator()

custom_story = {
    "id": "US-003",
    "title": "Product Catalog",
    "description": "As a user, I want to browse products with search and filters",
    "acceptance_criteria": [
        {"id": 1, "text": "Display product grid", "priority": "must-have"},
        {"id": 2, "text": "Search by name", "priority": "must-have"},
        {"id": 3, "text": "Filter by category", "priority": "should-have"}
    ],
    "tech_hints": {
        "requires_auth": False,
        "requires_database": True,
        "requires_api": True,
        "requires_ui": True,
        "complexity": "medium"
    }
}

result = orchestrator.process_story(custom_story)
```

## 🐳 Docker Mode (Optional)

Build and run all agents in Docker:

```powershell
# Build all agent images
docker-compose build

# Start everything
docker-compose up -d

# View logs
docker-compose logs -f planning-agent
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | OpenAI API key for LLM | - |
| `POSTGRES_HOST` | PostgreSQL host | postgres |
| `POSTGRES_PASSWORD` | Database password | autodev_secure_2025 |
| `REDIS_HOST` | Redis host | redis |
| `REDIS_PASSWORD` | Redis password | autodev_redis_2025 |

### Agent Ports

- Planning Agent: 8000
- Frontend Agent: 8001
- Backend Agent: 8002
- Database Agent: 8003
- Testing Agent: 8004
- n8n Workflow: 5678
- RabbitMQ Management: 15672

## 📈 Monitoring

### View All Logs

```powershell
docker-compose logs -f
```

### View Specific Service

```powershell
docker-compose logs -f planning-agent
```

### Database Metrics

```sql
-- Agent performance
SELECT agent_name, 
       COUNT(*) as total_executions,
       AVG(execution_time_seconds) as avg_time,
       SUM(CASE WHEN success THEN 1 ELSE 0 END) as successful
FROM agent_metrics
GROUP BY agent_name;
```

## 🎬 Demo Script

Run the automated demo:

```powershell
# Process all test stories
python -c "
import json
from orchestrator import SimpleOrchestrator

orchestrator = SimpleOrchestrator()

with open('test_stories.json') as f:
    stories = json.load(f)

for story in stories:
    result = orchestrator.process_story(story)
    print(f'\n✅ Completed: {story[\"title\"]}')
"
```

## 🚧 Troubleshooting

### Agents Not Starting

```powershell
# Check if ports are available
netstat -an | findstr "8000 8001 8002 8003 8004"

# Kill processes on ports if needed
Stop-Process -Id (Get-NetTCPConnection -LocalPort 8000).OwningProcess -Force
```

### Database Connection Issues

```powershell
# Restart PostgreSQL
docker-compose restart postgres

# Check PostgreSQL logs
docker-compose logs postgres
```

### Redis Connection Failed

```powershell
# Test Redis connection
docker exec -it autodev-redis redis-cli -a autodev_redis_2025 ping
```

## 🎯 Next Steps

1. **Add Real LLM Integration**: Replace mock architecture with OpenAI calls
2. **Build Dashboard**: Create React monitoring UI
3. **Setup n8n**: Import visual workflow orchestration
4. **Add More Agents**: Legacy analyzer, integration agent
5. **Enhance Testing**: Run actual pytest and Jest tests

## 📝 API Examples

### Planning Agent

```bash
curl -X POST http://localhost:8000/agents/planning \
  -H "Content-Type: application/json" \
  -d '{
    "story_id": "US-001",
    "session_id": "session_123",
    "title": "User Login",
    "description": "User authentication system",
    "acceptance_criteria": [],
    "tech_hints": {
      "requires_auth": true,
      "requires_database": true
    },
    "project_id": "demo"
  }'
```

### Frontend Agent

```bash
curl -X POST http://localhost:8001/agents/frontend \
  -H "Content-Type: application/json" \
  -d '{
    "task_id": "fe_001",
    "story_id": "US-001",
    "session_id": "session_123",
    "components": ["LoginForm", "Dashboard"]
  }'
```

## 🤝 Contributing

This is a prototype/demo project. Enhancements welcome!

## 📄 License

MIT License - Free to use for hackathons and demos

## 🎉 Success Checklist

- [ ] Docker containers running (postgres, redis, rabbitmq)
- [ ] All 5 agents responding to health checks
- [ ] Orchestrator successfully processes sample story
- [ ] Database logs show execution records
- [ ] Redis cache contains architecture data
- [ ] Generated code saved to database
- [ ] All agent API docs accessible at `/docs`

---

**Built for AutoDev Hackathon 2025** 🚀
