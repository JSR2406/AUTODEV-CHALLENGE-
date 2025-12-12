# n8n Workflow Placeholder

This directory will contain n8n workflow definitions for advanced orchestration.

## Quick Setup (Optional)

1. Start n8n:
   ```powershell
   docker-compose up -d n8n
   ```

2. Access n8n:
   - URL: http://localhost:5678
   - Username: admin
   - Password: autodev2025

3. Import workflow:
   - Click "+" to create new workflow
   - Add HTTP Request nodes for each agent
   - Connect them in sequence
   - Save and activate

## Workflow Structure

```
Trigger (Webhook)
  ↓
Planning Agent (HTTP Request)
  ↓
Database Agent (HTTP Request)
  ↓
Backend Agent (HTTP Request)
  ↓
Frontend Agent (HTTP Request)
  ↓
Testing Agent (HTTP Request)
  ↓
Response (Webhook Response)
```

## For Now

Use the Python orchestrator (`orchestrator.py`) for demo purposes.
n8n integration is optional for production deployments.
