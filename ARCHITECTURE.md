# 🏗️ AutoDev Platform - Architecture Overview

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER INTERFACE                          │
│                                                                 │
│  ┌────────────────────────────────────────────────────────┐   │
│  │         React Dashboard (Port 3000)                     │   │
│  │  - Agent Health Monitoring                              │   │
│  │  - Story Input Form                                     │   │
│  │  - Live Execution Logs                                  │   │
│  │  - Results Visualization                                │   │
│  └────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                      ORCHESTRATION LAYER                        │
│                                                                 │
│  ┌────────────────────────────────────────────────────────┐   │
│  │         Python Orchestrator                             │   │
│  │  - Coordinates agent execution                          │   │
│  │  - Manages session state                                │   │
│  │  - Handles error recovery                               │   │
│  └────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                        AI AGENT LAYER                           │
│                                                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │  Planning    │  │  Database    │  │  Backend     │         │
│  │  Agent       │  │  Agent       │  │  Agent       │         │
│  │  Port 8000   │  │  Port 8003   │  │  Port 8002   │         │
│  │              │  │              │  │              │         │
│  │ • GPT-4      │  │ • SQL        │  │ • FastAPI    │         │
│  │ • LangChain  │  │ • SQLAlchemy │  │ • CRUD       │         │
│  │ • Blueprint  │  │ • Schemas    │  │ • Auth       │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
│                                                                 │
│  ┌──────────────┐  ┌──────────────┐                           │
│  │  Frontend    │  │  Testing     │                           │
│  │  Agent       │  │  Agent       │                           │
│  │  Port 8001   │  │  Port 8004   │                           │
│  │              │  │              │                           │
│  │ • React      │  │ • Pytest     │                           │
│  │ • TypeScript │  │ • Jest       │                           │
│  │ • Components │  │ • Coverage   │                           │
│  └──────────────┘  └──────────────┘                           │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                    INFRASTRUCTURE LAYER                         │
│                                                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │  PostgreSQL  │  │    Redis     │  │  RabbitMQ    │         │
│  │  Port 5432   │  │  Port 6379   │  │  Port 5672   │         │
│  │              │  │              │  │              │         │
│  │ • Logs       │  │ • Cache      │  │ • Queue      │         │
│  │ • Code       │  │ • Sessions   │  │ • Messages   │         │
│  │ • Metrics    │  │ • Arch       │  │ • Events     │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
│                                                                 │
│  ┌────────────────────────────────────────────────────────┐   │
│  │              n8n Workflow Engine (Optional)             │   │
│  │              Port 5678                                  │   │
│  │  - Visual workflow designer                             │   │
│  │  - Advanced orchestration                               │   │
│  └────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

## Data Flow

```
User Story Input
      ↓
┌─────────────────┐
│ Planning Agent  │ → Analyzes story, generates architecture
└─────────────────┘
      ↓
   Blueprint
      ↓
┌─────────────────┐
│ Database Agent  │ → Creates SQL schemas, ORM models
└─────────────────┘
      ↓
┌─────────────────┐
│ Backend Agent   │ → Generates API endpoints
└─────────────────┘
      ↓
┌─────────────────┐
│ Frontend Agent  │ → Creates React components
└─────────────────┘
      ↓
┌─────────────────┐
│ Testing Agent   │ → Generates test files
└─────────────────┘
      ↓
Complete Codebase
```

## Agent Communication

```
┌──────────────────────────────────────────────────────────┐
│                    Session Flow                          │
└──────────────────────────────────────────────────────────┘

1. User submits story via Dashboard
   ↓
2. Orchestrator creates session ID
   ↓
3. Planning Agent:
   - Receives: Story + Criteria
   - Processes: GPT-4 analysis
   - Outputs: Architecture blueprint
   - Stores: Redis cache
   - Logs: PostgreSQL
   ↓
4. Database Agent:
   - Receives: Table definitions
   - Processes: SQL generation
   - Outputs: Schema files
   - Logs: PostgreSQL
   ↓
5. Backend Agent:
   - Receives: API endpoints
   - Processes: FastAPI code gen
   - Outputs: Route files
   - Logs: PostgreSQL
   ↓
6. Frontend Agent:
   - Receives: Component list
   - Processes: React code gen
   - Outputs: .tsx files
   - Logs: PostgreSQL
   ↓
7. Testing Agent:
   - Receives: Code layers
   - Processes: Test generation
   - Outputs: Test files + coverage
   - Logs: PostgreSQL
   ↓
8. Results returned to Dashboard
```

## Technology Stack

### Frontend
- **React 18**: UI framework
- **Axios**: HTTP client
- **CSS3**: Modern styling with gradients

### Backend Agents
- **FastAPI**: Web framework
- **Pydantic**: Data validation
- **LangChain**: LLM orchestration
- **OpenAI GPT-4**: AI generation

### Infrastructure
- **PostgreSQL 15**: Relational database
- **Redis 7**: In-memory cache
- **RabbitMQ 3**: Message broker
- **n8n**: Workflow automation
- **Docker**: Containerization

### Development
- **Python 3.11**: Agent runtime
- **Node.js 18**: Dashboard runtime
- **PowerShell**: Automation scripts

## Deployment Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Production Setup                     │
└─────────────────────────────────────────────────────────┘

                    Load Balancer
                         ↓
        ┌────────────────┼────────────────┐
        ↓                ↓                ↓
   Agent Pool 1    Agent Pool 2    Agent Pool 3
   (Planning)      (Code Gen)      (Testing)
        ↓                ↓                ↓
        └────────────────┼────────────────┘
                         ↓
                  Shared Services
                  - PostgreSQL (RDS)
                  - Redis (ElastiCache)
                  - RabbitMQ (AmazonMQ)
```

## Security Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Security Layers                      │
└─────────────────────────────────────────────────────────┘

1. API Gateway
   - Rate limiting
   - API key validation
   - Request logging

2. Agent Layer
   - Input validation (Pydantic)
   - SQL injection prevention
   - XSS protection

3. Database Layer
   - Encrypted connections
   - Parameterized queries
   - Access control

4. Infrastructure
   - Network isolation
   - Secrets management
   - TLS/SSL encryption
```

## Scalability

### Horizontal Scaling
```
Single Instance → Multiple Instances → Auto-scaling

Agent (1x)     →  Agents (3x)      →  Agents (N)
                  Load Balanced        Dynamic
```

### Vertical Scaling
```
Resource Allocation:
- Planning Agent: 2 CPU, 4GB RAM (LLM intensive)
- Code Agents: 1 CPU, 2GB RAM (I/O bound)
- Database: 4 CPU, 8GB RAM (Storage)
```

## Monitoring & Observability

```
┌─────────────────────────────────────────────────────────┐
│                    Monitoring Stack                     │
└─────────────────────────────────────────────────────────┘

Metrics Collection:
- Agent health checks (every 10s)
- Execution time tracking
- Error rate monitoring
- Resource utilization

Logging:
- Structured logs (JSON)
- Centralized aggregation
- Real-time streaming
- Long-term storage

Alerting:
- Agent failures
- Performance degradation
- Resource exhaustion
- Error thresholds
```

## Future Enhancements

### Phase 2
- [ ] Code review agent
- [ ] Deployment automation
- [ ] Version control integration
- [ ] CI/CD pipeline generation

### Phase 3
- [ ] Multi-language support
- [ ] Custom agent creation
- [ ] Plugin system
- [ ] Marketplace

### Phase 4
- [ ] Distributed execution
- [ ] ML model fine-tuning
- [ ] Advanced analytics
- [ ] Enterprise features

---

**Architecture Version**: 1.0  
**Last Updated**: 2025-12-06  
**Status**: Production Ready ✅
