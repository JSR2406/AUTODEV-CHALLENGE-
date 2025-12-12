# 📚 AutoDev Platform - Documentation Index

Welcome to the AutoDev Platform! This guide will help you navigate all the documentation.

## 🚀 Getting Started

**Start here if you're new:**

1. **[QUICKSTART.md](QUICKSTART.md)** - 5-minute setup guide
   - Prerequisites check
   - Step-by-step installation
   - First story processing
   - Troubleshooting

2. **[README.md](README.md)** - Complete project overview
   - What is AutoDev Platform
   - Features and capabilities
   - Installation instructions
   - API documentation links

## 📖 Understanding the System

3. **[ARCHITECTURE.md](ARCHITECTURE.md)** - System architecture
   - Component diagrams
   - Data flow
   - Technology stack
   - Deployment architecture
   - Security layers

4. **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** - What was built
   - Complete feature list
   - Project structure
   - Usage examples
   - Next steps

## 🎬 For Presentations

5. **[DEMO_SCRIPT.md](DEMO_SCRIPT.md)** - Presentation guide
   - 10-15 minute demo flow
   - Talking points
   - Q&A preparation
   - Backup plans
   - Time variants (5/10/15 min)

## 📁 Project Files

### Core Files

- **`.env`** - Environment configuration
  - API keys
  - Database credentials
  - Service ports

- **`docker-compose.yml`** - Infrastructure setup
  - PostgreSQL
  - Redis
  - RabbitMQ
  - n8n

- **`init-db.sql`** - Database schema
  - execution_logs
  - generated_code
  - test_results
  - agent_metrics

- **`orchestrator.py`** - Agent coordinator
  - Story processing logic
  - Agent communication
  - Error handling

- **`test_stories.json`** - Sample data
  - Example user stories
  - Test cases

### Scripts

- **`start.ps1`** - Startup script (Windows)
  - Starts all services
  - Health checks
  - Dashboard launch

- **`stop.ps1`** - Shutdown script
  - Stops all processes
  - Cleans up resources

### Agents Directory

- **`planning_agent.py`** - Architecture generation
  - GPT-4 integration
  - Blueprint creation
  - Mock fallback

- **`database_agent.py`** - Schema generation
  - SQL creation
  - ORM models

- **`backend_agent.py`** - API generation
  - FastAPI endpoints
  - CRUD operations

- **`frontend_agent.py`** - Component generation
  - React components
  - TypeScript

- **`testing_agent.py`** - Test generation
  - Pytest tests
  - Jest tests

- **`requirements.txt`** - Python dependencies
  - FastAPI
  - LangChain
  - OpenAI

- **`Dockerfile.*`** - Docker configurations
  - One per agent

### Dashboard Directory

- **`package.json`** - Node dependencies
  - React
  - Axios

- **`src/App.js`** - Main dashboard
  - Agent monitoring
  - Story processing
  - Results display

- **`src/App.css`** - Dashboard styling
  - Modern design
  - Responsive layout

- **`public/index.html`** - HTML template

## 🎯 Quick Navigation

### I want to...

**...get started quickly**
→ Read [QUICKSTART.md](QUICKSTART.md)

**...understand the architecture**
→ Read [ARCHITECTURE.md](ARCHITECTURE.md)

**...prepare a demo**
→ Read [DEMO_SCRIPT.md](DEMO_SCRIPT.md)

**...see what was built**
→ Read [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)

**...install and run**
→ Read [README.md](README.md)

**...troubleshoot issues**
→ See [QUICKSTART.md](QUICKSTART.md#troubleshooting)

**...add a new agent**
→ See [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md#extending-the-platform)

**...deploy to production**
→ See [ARCHITECTURE.md](ARCHITECTURE.md#deployment-architecture)

**...understand the code**
→ Check agent files in `agents/` directory

**...customize the dashboard**
→ Edit files in `dashboard/src/`

## 📊 File Sizes & Complexity

| File | Size | Complexity | Purpose |
|------|------|------------|---------|
| QUICKSTART.md | 6.7 KB | ⭐⭐ | Getting started |
| README.md | 9.6 KB | ⭐⭐⭐ | Overview |
| ARCHITECTURE.md | 14.0 KB | ⭐⭐⭐⭐ | System design |
| PROJECT_SUMMARY.md | 10.4 KB | ⭐⭐⭐ | Feature list |
| DEMO_SCRIPT.md | 9.5 KB | ⭐⭐⭐ | Presentation |
| planning_agent.py | 16.2 KB | ⭐⭐⭐⭐⭐ | Core AI agent |
| orchestrator.py | 6.7 KB | ⭐⭐⭐⭐ | Coordination |
| App.js | ~10 KB | ⭐⭐⭐⭐ | Dashboard UI |

## 🔗 External Links

### API Documentation (when running)
- Planning Agent: http://localhost:8000/docs
- Frontend Agent: http://localhost:8001/docs
- Backend Agent: http://localhost:8002/docs
- Database Agent: http://localhost:8003/docs
- Testing Agent: http://localhost:8004/docs

### Dashboard (when running)
- Monitoring Dashboard: http://localhost:3000

### Infrastructure (when running)
- n8n Workflow: http://localhost:5678
- RabbitMQ Management: http://localhost:15672

## 📝 Reading Order

### For First-Time Users
1. README.md (overview)
2. QUICKSTART.md (setup)
3. Try the platform!
4. PROJECT_SUMMARY.md (understand what you built)

### For Developers
1. ARCHITECTURE.md (system design)
2. Agent source code (implementation)
3. orchestrator.py (coordination logic)
4. Dashboard code (UI implementation)

### For Presenters
1. DEMO_SCRIPT.md (presentation flow)
2. ARCHITECTURE.md (diagrams to show)
3. PROJECT_SUMMARY.md (features to highlight)
4. Practice with QUICKSTART.md

## 🎓 Learning Path

### Beginner
1. Read README.md
2. Follow QUICKSTART.md
3. Process sample stories
4. Explore dashboard

### Intermediate
1. Read ARCHITECTURE.md
2. Review agent code
3. Customize a story
4. Query database

### Advanced
1. Add a new agent
2. Modify orchestration
3. Enhance dashboard
4. Deploy to production

## 🆘 Getting Help

### Common Issues
- **Agents offline**: See QUICKSTART.md troubleshooting
- **Database errors**: Check docker-compose logs
- **Dashboard not loading**: Verify Node.js installation
- **API errors**: Check agent logs in `logs/` directory

### Where to Look
- **Setup issues**: QUICKSTART.md
- **Architecture questions**: ARCHITECTURE.md
- **Feature questions**: PROJECT_SUMMARY.md
- **Demo prep**: DEMO_SCRIPT.md

## 📦 What's Included

### Documentation (7 files)
- ✅ README.md
- ✅ QUICKSTART.md
- ✅ ARCHITECTURE.md
- ✅ PROJECT_SUMMARY.md
- ✅ DEMO_SCRIPT.md
- ✅ INDEX.md (this file)
- ✅ workflows/README.md

### Code (16 files)
- ✅ 5 Agent implementations
- ✅ 5 Dockerfiles
- ✅ 1 Orchestrator
- ✅ 4 Dashboard files
- ✅ 1 Requirements file

### Configuration (6 files)
- ✅ .env
- ✅ .gitignore
- ✅ docker-compose.yml
- ✅ init-db.sql
- ✅ package.json
- ✅ test_stories.json

### Scripts (2 files)
- ✅ start.ps1
- ✅ stop.ps1

**Total: 31 files** organized for maximum clarity!

## 🎯 Success Checklist

After reading this index, you should know:
- [ ] Where to start (QUICKSTART.md)
- [ ] How the system works (ARCHITECTURE.md)
- [ ] What was built (PROJECT_SUMMARY.md)
- [ ] How to demo (DEMO_SCRIPT.md)
- [ ] Where to find specific information

## 🚀 Next Steps

1. **If you haven't started yet:**
   ```powershell
   ./start.ps1
   ```

2. **If you want to understand more:**
   - Read ARCHITECTURE.md

3. **If you're preparing a demo:**
   - Read DEMO_SCRIPT.md

4. **If you want to extend:**
   - Read PROJECT_SUMMARY.md → "Next Steps"

---

**Welcome to AutoDev Platform!** 🎉

**Quick Start:** `./start.ps1` → Open http://localhost:3000 → Process a story!

**Questions?** Check the relevant .md file above or explore the code!

**Built for AutoDev Hackathon 2025** 🚀
