"""
Frontend Agent - Generates React components
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict
import os
import redis
import json
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Frontend Agent")

redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST", "localhost"),
    port=6379,
    password=os.getenv("REDIS_PASSWORD", ""),
    decode_responses=True
)

class FrontendTask(BaseModel):
    task_id: str
    story_id: str
    session_id: str
    components: List[str]

class FrontendResponse(BaseModel):
    status: str
    task_id: str
    generated_files: List[Dict[str, str]]

def generate_react_component(component_name: str) -> str:
    """Generate a React component template"""
    
    template = f"""import React, {{ useState, useEffect }} from 'react';
import {{ useNavigate }} from 'react-router-dom';

interface {component_name}Props {{
  onSuccess?: () => void;
}}

export const {component_name}: React.FC<{component_name}Props> = ({{ onSuccess }}) => {{
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const navigate = useNavigate();

  useEffect(() => {{
    // Component initialization
    console.log('{component_name} mounted');
  }}, []);

  const handleSubmit = async (e: React.FormEvent) => {{
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {{
      // Add your API call here
      const response = await fetch('/api/endpoint', {{
        method: 'POST',
        headers: {{ 'Content-Type': 'application/json' }},
        body: JSON.stringify({{ /* data */ }})
      }});

      if (!response.ok) throw new Error('Request failed');
      
      const data = await response.json();
      console.log('Success:', data);
      
      if (onSuccess) onSuccess();
    }} catch (err) {{
      setError(err instanceof Error ? err.message : 'Unknown error');
    }} finally {{
      setLoading(false);
    }}
  }};

  return (
    <div className="container mx-auto p-4">
      <h2 className="text-2xl font-bold mb-4">{component_name}</h2>
      
      {{error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
          {{error}}
        </div>
      )}}

      <form onSubmit={{handleSubmit}} className="space-y-4">
        <div>
          <label className="block text-sm font-medium mb-2">
            Input Field
          </label>
          <input
            type="text"
            className="w-full px-3 py-2 border rounded-md"
            placeholder="Enter value"
            required
          />
        </div>

        <button
          type="submit"
          disabled={{loading}}
          className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 disabled:opacity-50"
        >
          {{loading ? 'Processing...' : 'Submit'}}
        </button>
      </form>
    </div>
  );
}};
"""
    return template

@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "service": "frontend-agent",
        "timestamp": datetime.utcnow().isoformat()
    }

@app.post("/agents/frontend", response_model=FrontendResponse)
async def generate_frontend(task: FrontendTask):
    logger.info(f"Frontend generation for task: {task.task_id}")
    
    try:
        generated_files = []
        
        for component_name in task.components:
            code = generate_react_component(component_name)
            
            generated_files.append({
                "file_path": f"src/components/{component_name}.tsx",
                "content": code,
                "language": "typescript"
            })
        
        logger.info(f"Generated {len(generated_files)} components")
        
        return FrontendResponse(
            status="success",
            task_id=task.task_id,
            generated_files=generated_files
        )
        
    except Exception as e:
        logger.error(f"Frontend generation failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
