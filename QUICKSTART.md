# 🚀 AutoDev Platform - Quick Start Guide

## ⚡ 5-Minute Setup

### Step 1: Prerequisites Check

Ensure you have:
- ✅ Docker Desktop installed and running
- ✅ Python 3.11+ installed
- ✅ Node.js 18+ installed (for dashboard)
- ✅ 8GB+ RAM available

### Step 2: Start the Platform

Open PowerShell in the project directory and run:

```powershell
./start.ps1
```

This will:
1. Start PostgreSQL, Redis, and RabbitMQ
2. Install Python dependencies
3. Launch all 5 AI agents
4. Start the monitoring dashboard
5. Perform health checks

**Wait for:** "✅ AutoDev Platform is READY!"

### Step 3: Access the Dashboard

Open your browser to: **http://localhost:3000**

You should see:
- ✅ All 5 agents showing as "healthy"
- 📝 Story input form
- 📊 Live execution logs

### Step 4: Process Your First Story

In the dashboard:

1. **Enter a story title:** "User Authentication"
2. **Add description:** "As a user, I want to log in with email and password"
3. **Add criteria:** (one per line)
   ```
   User can enter email and password
   System validates credentials
   JWT token returned on success
   ```
4. **Click:** "🚀 Process Story"

Watch the magic happen! You'll see:
- 📋 Planning Agent generating architecture
- 🗄️ Database Agent creating schemas
- ⚙️ Backend Agent generating APIs
- 🎨 Frontend Agent creating components
- 🧪 Testing Agent generating tests

### Step 5: View Results

After processing completes (~10-30 seconds), you'll see:
- Database tables generated
- API endpoints created
- React components scaffolded
- Test coverage report

## 🔍 Verify Everything Works

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

All should return: `{"status":"healthy",...}`

### Test via CLI

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

### Query the Database

```powershell
docker exec -it autodev-postgres psql -U postgres -d autodev_platform

# Inside psql:
SELECT story_id, agent_name, status, created_at 
FROM execution_logs 
ORDER BY created_at DESC 
LIMIT 10;
```

### Check Redis Cache

```powershell
docker exec -it autodev-redis redis-cli -a autodev_redis_2025

# Inside redis-cli:
KEYS *
```

## 🎯 What to Try Next

### 1. Process Different Stories

Try these examples:

**E-commerce Product Catalog:**
```
Title: Product Catalog
Description: As a customer, I want to browse and search products
Criteria:
- Display product grid with images
- Search by name and category
- Filter by price range
- Sort by price, name, rating
```

**Task Management:**
```
Title: Task Management
Description: As a user, I want to create and track tasks
Criteria:
- Create tasks with title and description
- Mark tasks as complete
- Set due dates
- Assign priority levels
```

**Blog System:**
```
Title: Blog Platform
Description: As an author, I want to publish blog posts
Criteria:
- Create posts with rich text
- Add tags and categories
- Schedule publication
- Allow comments
```

### 2. Enable Real AI (Optional)

If you have an OpenAI API key:

1. Edit `.env`:
   ```
   OPENAI_API_KEY=sk-your-actual-key-here
   ```

2. Restart agents:
   ```powershell
   ./stop.ps1
   ./start.ps1
   ```

3. Now the Planning Agent will use GPT-4 for smarter architecture!

### 3. Explore API Documentation

Visit these URLs to see interactive API docs:

- http://localhost:8000/docs - Planning Agent
- http://localhost:8001/docs - Frontend Agent
- http://localhost:8002/docs - Backend Agent
- http://localhost:8003/docs - Database Agent
- http://localhost:8004/docs - Testing Agent

### 4. View Logs

```powershell
# Real-time logs
Get-Content logs/planning.log -Tail 20 -Wait

# Docker logs
docker-compose logs -f postgres
```

## 🛑 Stopping the Platform

When you're done:

```powershell
./stop.ps1
```

This will cleanly shut down:
- All agent processes
- Docker containers
- Dashboard server

## ❓ Troubleshooting

### Agents Not Starting

**Problem:** Agents show as "offline" in dashboard

**Solution:**
```powershell
# Check if ports are in use
netstat -an | findstr "8000 8001 8002 8003 8004"

# Kill processes on those ports
Stop-Process -Id (Get-NetTCPConnection -LocalPort 8000).OwningProcess -Force
```

### Database Connection Failed

**Problem:** "Database not ready" message

**Solution:**
```powershell
# Restart PostgreSQL
docker-compose restart postgres

# Wait 10 seconds
Start-Sleep -Seconds 10

# Check status
docker-compose ps
```

### Dashboard Not Loading

**Problem:** http://localhost:3000 doesn't open

**Solution:**
```powershell
# Check if Node is running
Get-Process node

# If not, start manually
cd dashboard
npm start
```

### Redis Connection Error

**Problem:** "Redis connection failed" in logs

**Solution:**
```powershell
# Restart Redis
docker-compose restart redis

# Test connection
docker exec -it autodev-redis redis-cli -a autodev_redis_2025 ping
```

## 📊 Success Checklist

After setup, verify:

- [ ] Docker containers running: `docker-compose ps`
- [ ] All 5 agents healthy: Check dashboard
- [ ] Dashboard accessible: http://localhost:3000
- [ ] Can process a story successfully
- [ ] Database has execution logs
- [ ] Redis has cached data
- [ ] API docs accessible

## 🎉 You're Ready!

Your AutoDev Platform is now fully operational!

**Next Steps:**
1. Process multiple stories
2. Explore generated code
3. Customize agent behavior
4. Add your own agents
5. Integrate with CI/CD

**Need Help?**
- Check logs in `logs/` directory
- Review agent API docs
- Query database for execution history

---

**Built for AutoDev Hackathon 2025** 🚀
