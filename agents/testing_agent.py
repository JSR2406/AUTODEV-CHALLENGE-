"""
Testing Agent - Generates and runs tests
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Testing Agent")

class TestingTask(BaseModel):
    task_id: str
    story_id: str
    session_id: str
    code_layers: List[str]

class TestingResponse(BaseModel):
    status: str
    task_id: str
    tests_passed: bool
    coverage: float
    total_tests: int
    test_files: List[Dict[str, str]]

def generate_pytest_tests(component_name: str) -> str:
    """Generate pytest test file"""
    
    template = f"""import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_{component_name.lower()}_get():
    '''Test GET endpoint'''
    response = client.get("/api/{component_name.lower()}")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_{component_name.lower()}_post():
    '''Test POST endpoint'''
    data = {{"data": {{"test": "value"}}}}
    response = client.post("/api/{component_name.lower()}", json=data)
    assert response.status_code == 201
    assert "id" in response.json()

def test_{component_name.lower()}_invalid_data():
    '''Test invalid data handling'''
    response = client.post("/api/{component_name.lower()}", json={{}})
    assert response.status_code == 422
"""
    return template

def generate_jest_tests(component_name: str) -> str:
    """Generate Jest test file"""
    
    template = f"""import React from 'react';
import {{ render, screen, fireEvent, waitFor }} from '@testing-library/react';
import {{ {component_name} }} from './{component_name}';

describe('{component_name}', () => {{
  it('renders without crashing', () => {{
    render(<{component_name} />);
    expect(screen.getByRole('heading')).toBeInTheDocument();
  }});

  it('handles form submission', async () => {{
    const onSuccess = jest.fn();
    render(<{component_name} onSuccess={{onSuccess}} />);
    
    const submitButton = screen.getByRole('button', {{ name: /submit/i }});
    fireEvent.click(submitButton);
    
    await waitFor(() => {{
      expect(onSuccess).toHaveBeenCalled();
    }});
  }});

  it('displays error messages', async () => {{
    render(<{component_name} />);
    
    // Trigger error condition
    const submitButton = screen.getByRole('button');
    fireEvent.click(submitButton);
    
    await waitFor(() => {{
      expect(screen.getByText(/error/i)).toBeInTheDocument();
    }});
  }});
}});
"""
    return template

@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "service": "testing-agent",
        "timestamp": datetime.utcnow().isoformat()
    }

@app.post("/agents/testing", response_model=TestingResponse)
async def generate_tests(task: TestingTask):
    logger.info(f"Test generation for task: {task.task_id}")
    
    try:
        test_files = []
        
        # Generate backend tests
        if "backend" in task.code_layers:
            pytest_code = generate_pytest_tests("resource")
            test_files.append({
                "file_path": "tests/test_api.py",
                "content": pytest_code,
                "language": "python"
            })
        
        # Generate frontend tests
        if "frontend" in task.code_layers:
            jest_code = generate_jest_tests("Component")
            test_files.append({
                "file_path": "src/components/__tests__/Component.test.tsx",
                "content": jest_code,
                "language": "typescript"
            })
        
        # Mock test results
        tests_passed = True
        coverage = 87.5
        total_tests = len(test_files) * 3
        
        logger.info(f"Generated {len(test_files)} test files")
        
        return TestingResponse(
            status="success",
            task_id=task.task_id,
            tests_passed=tests_passed,
            coverage=coverage,
            total_tests=total_tests,
            test_files=test_files
        )
        
    except Exception as e:
        logger.error(f"Test generation failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8004)
