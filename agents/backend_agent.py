"""
Backend Agent - Generates FastAPI endpoints
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Backend Agent")

class BackendTask(BaseModel):
    task_id: str
    story_id: str
    session_id: str
    endpoints: List[Dict]

class BackendResponse(BaseModel):
    status: str
    task_id: str
    generated_files: List[Dict[str, str]]

def generate_fastapi_endpoint(endpoint: Dict) -> str:
    """Generate FastAPI endpoint code"""
    
    path = endpoint.get("path", "/api/resource")
    method = endpoint.get("method", "GET").upper()
    auth_required = endpoint.get("auth_required", False)
    
    template = f"""from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

router = APIRouter(prefix="{path.rsplit('/', 1)[0]}", tags=["{path.split('/')[2] if len(path.split('/')) > 2 else 'api'}"])

# Models
class RequestModel(BaseModel):
    data: dict
    
class ResponseModel(BaseModel):
    id: int
    data: dict
    created_at: datetime

"""

    if auth_required:
        template += """# Authentication dependency
async def get_current_user(token: str = Depends(oauth2_scheme)):
    # Implement JWT validation
    return {{"user_id": 1}}

"""

    if method == "GET":
        template += f"""@router.get("{path.split(path.rsplit('/', 1)[0])[-1]}", response_model=List[ResponseModel])
async def get_items({f"current_user = Depends(get_current_user)" if auth_required else ""}):
    '''Retrieve all items'''
    # TODO: Implement database query
    return []
"""
    
    elif method == "POST":
        template += f"""@router.post("{path.split(path.rsplit('/', 1)[0])[-1]}", response_model=ResponseModel, status_code=status.HTTP_201_CREATED)
async def create_item(
    item: RequestModel,
    {f"current_user = Depends(get_current_user)" if auth_required else ""}
):
    '''Create a new item'''
    # TODO: Implement database insert
    return ResponseModel(
        id=1,
        data=item.data,
        created_at=datetime.utcnow()
    )
"""
    
    return template

@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "service": "backend-agent",
        "timestamp": datetime.utcnow().isoformat()
    }

@app.post("/agents/backend", response_model=BackendResponse)
async def generate_backend(task: BackendTask):
    logger.info(f"Backend generation for task: {task.task_id}")
    
    try:
        generated_files = []
        
        for endpoint in task.endpoints:
            code = generate_fastapi_endpoint(endpoint)
            path_name = endpoint["path"].replace("/", "_").replace("{", "").replace("}", "")
            
            generated_files.append({
                "file_path": f"app/routes{path_name}.py",
                "content": code,
                "language": "python"
            })
        
        logger.info(f"Generated {len(generated_files)} endpoints")
        
        return BackendResponse(
            status="success",
            task_id=task.task_id,
            generated_files=generated_files
        )
        
    except Exception as e:
        logger.error(f"Backend generation failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)
