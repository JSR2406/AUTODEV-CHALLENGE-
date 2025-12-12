"""
Planning Agent - Generates architecture blueprints from user stories
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Dict, Optional
import os
import json
import redis
import asyncpg
import logging
from datetime import datetime

# Direct OpenAI import instead of LangChain (Python 3.12 compatibility)
try:
    from openai import AsyncOpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    logger.warning("OpenAI not available, will use mock generation only")

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Planning Agent", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Redis client
redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST", "localhost"),
    port=6379,
    password=os.getenv("REDIS_PASSWORD", ""),
    decode_responses=True
)

# Initialize OpenAI client (only if API key is provided)
openai_client = None
if OPENAI_AVAILABLE and os.getenv("OPENAI_API_KEY") and os.getenv("OPENAI_API_KEY") != "your-openai-key-here":
    try:
        openai_client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        logger.info("OpenAI client initialized successfully")
    except Exception as e:
        logger.warning(f"Failed to initialize OpenAI client: {e}")
        openai_client = None
else:
    logger.info("No OpenAI API key provided, will use mock architecture generation")

db_pool = None

# ============================================
# MODELS
# ============================================

class AcceptanceCriterion(BaseModel):
    id: int
    text: str
    priority: str = "must-have"

class TechHints(BaseModel):
    requires_auth: bool = False
    requires_database: bool = True
    requires_api: bool = True
    requires_ui: bool = True
    complexity: str = "medium"

class PlanningRequest(BaseModel):
    story_id: str
    session_id: str
    title: str
    description: str
    acceptance_criteria: List[AcceptanceCriterion]
    tech_hints: TechHints
    project_id: str

class TableColumn(BaseModel):
    name: str
    type: str
    constraints: Optional[str] = None

class DatabaseTable(BaseModel):
    name: str
    columns: List[TableColumn]

class DatabaseSchema(BaseModel):
    tables: List[DatabaseTable]
    relationships: List[str] = []

class APIEndpoint(BaseModel):
    path: str
    method: str
    auth_required: bool = True
    description: Optional[str] = None

class BackendArchitecture(BaseModel):
    endpoints: List[APIEndpoint]
    middleware: List[str] = ["auth", "validation", "logging"]

class FrontendArchitecture(BaseModel):
    components: List[str]
    state_management: str = "zustand"
    routing: str = "react-router"

class DependencyEdge(BaseModel):
    from_node: str
    to: str
    
    model_config = {"populate_by_name": True}

class DependencyGraph(BaseModel):
    nodes: List[str]
    edges: List[DependencyEdge]

class Architecture(BaseModel):
    database: DatabaseSchema
    backend: BackendArchitecture
    frontend: FrontendArchitecture
    dependency_graph: DependencyGraph

class PlanningResponse(BaseModel):
    status: str
    story_id: str
    session_id: str
    architecture: Architecture
    execution_time_seconds: float

# ============================================
# DATABASE
# ============================================

async def init_db():
    global db_pool
    if not db_pool:
        db_pool = await asyncpg.create_pool(
            host=os.getenv("POSTGRES_HOST", "localhost"),
            port=5432,
            database=os.getenv("POSTGRES_DB", "autodev_platform"),
            user=os.getenv("POSTGRES_USER", "postgres"),
            password=os.getenv("POSTGRES_PASSWORD", ""),
            min_size=2,
            max_size=10
        )
    return db_pool

async def log_execution(story_id: str, agent_name: str, status: str, output: Dict):
    pool = await init_db()
    async with pool.acquire() as conn:
        await conn.execute(
            """
            INSERT INTO execution_logs 
            (story_id, agent_name, status, output, created_at)
            VALUES ($1, $2, $3, $4, NOW())
            """,
            story_id, agent_name, status, json.dumps(output)
        )

# ============================================
# ARCHITECTURE GENERATION
# ============================================

async def generate_real_architecture(request: PlanningRequest) -> Architecture:
    """
    Generate architecture using real OpenAI API (direct, no LangChain)
    """
    
    logger.info(f"Generating real architecture with OpenAI for: {request.title}")
    
    # Build comprehensive prompt
    criteria_text = "\n".join([
        f"{i+1}. [{c.priority.upper()}] {c.text}"
        for i, c in enumerate(request.acceptance_criteria)
    ])
    
    system_prompt = """You are an expert software architect. Analyze user stories and generate comprehensive technical architecture blueprints.

**Output Requirements:**
- Database schema with proper normalization
- RESTful API design with proper HTTP methods
- React component hierarchy
- Dependency graph for execution order

**Quality Standards:**
- Security-first design (JWT, input validation)
- Scalable database design
- Modern React patterns (hooks, composition)
- WCAG 2.1 AA accessibility

**CRITICAL: Output ONLY valid JSON. No markdown, no explanations.**"""
    
    user_prompt = f"""**User Story:**
Title: {request.title}
Description: {request.description}

**Acceptance Criteria:**
{criteria_text}

**Technical Context:**
- Authentication Required: {request.tech_hints.requires_auth}
- Database Required: {request.tech_hints.requires_database}
- API Required: {request.tech_hints.requires_api}
- UI Required: {request.tech_hints.requires_ui}
- Complexity: {request.tech_hints.complexity}

Generate a complete architecture blueprint as JSON with this exact structure:
{{
  "database": {{
    "tables": [
      {{
        "name": "table_name",
        "columns": [
          {{"name": "id", "type": "SERIAL", "constraints": "PRIMARY KEY"}},
          {{"name": "email", "type": "VARCHAR(255)", "constraints": "UNIQUE NOT NULL"}}
        ]
      }}
    ],
    "relationships": ["users.id -> sessions.user_id"]
  }},
  "backend": {{
    "endpoints": [
      {{
        "path": "/api/users",
        "method": "POST",
        "auth_required": true,
        "description": "Create new user"
      }}
    ],
    "middleware": ["auth", "validation", "logging"]
  }},
  "frontend": {{
    "components": ["LoginForm", "Dashboard"],
    "state_management": "zustand",
    "routing": "react-router"
  }},
  "dependency_graph": {{
    "nodes": ["database", "backend", "frontend", "testing"],
    "edges": [
      {{"from_node": "database", "to": "backend"}},
      {{"from_node": "backend", "to": "frontend"}},
      {{"from_node": "frontend", "to": "testing"}}
    ]
  }}
}}"""
    
    try:
        response = await openai_client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.2,
            max_tokens=4096
        )
        
        # Extract JSON from response
        content = response.choices[0].message.content.strip()
        
        # Remove markdown code blocks if present
        if content.startswith("```"):
            content = content.split("```")[1]
            if content.startswith("json"):
                content = content[4:]
            content = content.strip()
        
        # Parse JSON
        architecture_data = json.loads(content)
        architecture = Architecture(**architecture_data)
        
        logger.info(f"Successfully generated architecture with {len(architecture.database.tables)} tables")
        return architecture
        
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse OpenAI JSON response: {e}")
        logger.error(f"Response content: {content[:500]}")
        
        # Fallback to mock if LLM fails
        logger.warning("Falling back to mock architecture generation")
        return generate_mock_architecture(request)
        
    except Exception as e:
        logger.error(f"OpenAI API call failed: {e}")
        # Fallback to mock
        return generate_mock_architecture(request)

def generate_mock_architecture(request: PlanningRequest) -> Architecture:
    """
    Generate mock architecture based on story requirements
    This is a SIMPLIFIED version for rapid prototyping
    Replace with real LLM calls later
    """
    
    logger.info(f"Generating mock architecture for: {request.title}")
    
    # Analyze requirements
    needs_users = "user" in request.description.lower() or "login" in request.description.lower()
    needs_auth = request.tech_hints.requires_auth or "auth" in request.description.lower()
    
    # Generate database schema
    tables = []
    
    if needs_users:
        tables.append(DatabaseTable(
            name="users",
            columns=[
                TableColumn(name="id", type="SERIAL", constraints="PRIMARY KEY"),
                TableColumn(name="email", type="VARCHAR(255)", constraints="UNIQUE NOT NULL"),
                TableColumn(name="password_hash", type="VARCHAR(255)", constraints="NOT NULL"),
                TableColumn(name="created_at", type="TIMESTAMP", constraints="DEFAULT NOW()")
            ]
        ))
    
    # Add feature-specific table based on title
    feature_name = request.title.lower().replace(" ", "_")
    tables.append(DatabaseTable(
        name=f"{feature_name}_data",
        columns=[
            TableColumn(name="id", type="SERIAL", constraints="PRIMARY KEY"),
            TableColumn(name="user_id", type="INTEGER", constraints="REFERENCES users(id)" if needs_users else None),
            TableColumn(name="data", type="JSONB"),
            TableColumn(name="created_at", type="TIMESTAMP", constraints="DEFAULT NOW()")
        ]
    ))
    
    database = DatabaseSchema(
        tables=tables,
        relationships=["users.id -> {}_data.user_id".format(feature_name)] if needs_users else []
    )
    
    # Generate backend API
    endpoints = []
    
    if needs_auth:
        endpoints.extend([
            APIEndpoint(path="/api/auth/login", method="POST", auth_required=False, description="User login"),
            APIEndpoint(path="/api/auth/register", method="POST", auth_required=False, description="User registration"),
        ])
    
    endpoints.extend([
        APIEndpoint(path=f"/api/{feature_name}", method="GET", auth_required=needs_auth, description=f"List {feature_name}"),
        APIEndpoint(path=f"/api/{feature_name}", method="POST", auth_required=needs_auth, description=f"Create {feature_name}"),
        APIEndpoint(path=f"/api/{feature_name}/{{id}}", method="GET", auth_required=needs_auth, description=f"Get {feature_name}"),
        APIEndpoint(path=f"/api/{feature_name}/{{id}}", method="PUT", auth_required=needs_auth, description=f"Update {feature_name}"),
        APIEndpoint(path=f"/api/{feature_name}/{{id}}", method="DELETE", auth_required=needs_auth, description=f"Delete {feature_name}"),
    ])
    
    backend = BackendArchitecture(
        endpoints=endpoints,
        middleware=["auth", "validation", "logging", "cors"] if needs_auth else ["validation", "logging", "cors"]
    )
    
    # Generate frontend components
    components = []
    
    if needs_auth:
        components.extend(["LoginForm", "RegisterForm", "AuthGuard"])
    
    # Title-based component
    title_words = request.title.split()
    main_component = "".join([w.capitalize() for w in title_words]) + "Component"
    
    components.extend([
        main_component,
        f"{main_component}List",
        f"{main_component}Form",
        "Navigation",
        "ErrorBoundary"
    ])
    
    frontend = FrontendArchitecture(
        components=components,
        state_management="zustand",
        routing="react-router"
    )
    
    # Dependency graph
    nodes = ["database", "backend", "frontend", "testing"]
    edges = [
        DependencyEdge(from_node="database", to="backend"),
        DependencyEdge(from_node="backend", to="frontend"),
        DependencyEdge(from_node="frontend", to="testing")
    ]
    
    dependency_graph = DependencyGraph(nodes=nodes, edges=edges)
    
    return Architecture(
        database=database,
        backend=backend,
        frontend=frontend,
        dependency_graph=dependency_graph
    )

# ============================================
# API ENDPOINTS
# ============================================

@app.on_event("startup")
async def startup():
    logger.info("Planning Agent starting...")
    try:
        await init_db()
        logger.info("Database connected")
    except Exception as e:
        logger.warning(f"Database connection failed (will retry on first request): {e}")
    
    try:
        redis_client.ping()
        logger.info("Redis connected")
    except Exception as e:
        logger.warning(f"Redis connection failed: {e}")

@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "service": "planning-agent",
        "timestamp": datetime.utcnow().isoformat()
    }

@app.post("/agents/planning", response_model=PlanningResponse)
async def create_planning(request: PlanningRequest):
    start_time = datetime.utcnow()
    logger.info(f"Planning request for story: {request.story_id}")
    
    try:
        # Log start
        await log_execution(
            request.story_id,
            "planning_agent",
            "started",
            {"request": request.dict()}
        )
        
        # Use real LLM if available, otherwise use mock
        if openai_client is not None:
            logger.info("Using real OpenAI API")
            architecture = await generate_real_architecture(request)
        else:
            logger.warning("Using mock architecture (no OpenAI key)")
            architecture = generate_mock_architecture(request)
        
        # Save to Redis
        redis_client.setex(
            f"architecture:{request.session_id}",
            3600,
            architecture.json()
        )
        
        execution_time = (datetime.utcnow() - start_time).total_seconds()
        
        # Log completion
        await log_execution(
            request.story_id,
            "planning_agent",
            "completed",
            {"architecture": architecture.dict()}
        )
        
        logger.info(f"Planning completed in {execution_time:.2f}s")
        
        return PlanningResponse(
            status="success",
            story_id=request.story_id,
            session_id=request.session_id,
            architecture=architecture,
            execution_time_seconds=execution_time
        )
        
    except Exception as e:
        logger.error(f"Planning failed: {str(e)}")
        await log_execution(
            request.story_id,
            "planning_agent",
            "failed",
            {"error": str(e)}
        )
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/agents/planning/{session_id}")
async def get_planning(session_id: str):
    try:
        arch_json = redis_client.get(f"architecture:{session_id}")
        if not arch_json:
            raise HTTPException(status_code=404, detail="Architecture not found")
        return json.loads(arch_json)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
