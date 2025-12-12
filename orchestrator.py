"""
Simple Orchestrator - Coordinates agents without n8n
Use this for testing before setting up n8n
"""

import requests
import json
import time
from typing import Dict

class SimpleOrchestrator:
    def __init__(self):
        self.planning_url = "http://localhost:8000"
        self.frontend_url = "http://localhost:8001"
        self.backend_url = "http://localhost:8002"
        self.database_url = "http://localhost:8003"
        self.testing_url = "http://localhost:8004"
    
    def process_story(self, story: Dict) -> Dict:
        """Process a user story end-to-end"""
        
        print(f"\n🚀 Processing Story: {story['title']}")
        print("=" * 60)
        
        # Step 1: Planning
        print("\n📋 Step 1: Planning Agent...")
        planning_request = {
            "story_id": story["id"],
            "session_id": f"session_{story['id']}_{int(time.time())}",
            "title": story["title"],
            "description": story["description"],
            "acceptance_criteria": story.get("acceptance_criteria", []),
            "tech_hints": story.get("tech_hints", {
                "requires_auth": False,
                "requires_database": True,
                "requires_api": True,
                "requires_ui": True,
                "complexity": "medium"
            }),
            "project_id": "demo-project"
        }
        
        try:
            response = requests.post(
                f"{self.planning_url}/agents/planning",
                json=planning_request,
                timeout=30
            )
            response.raise_for_status()
            planning_result = response.json()
            print(f"✅ Planning completed in {planning_result['execution_time_seconds']:.2f}s")
            
            architecture = planning_result["architecture"]
            session_id = planning_result["session_id"]
            
        except Exception as e:
            print(f"❌ Planning failed: {str(e)}")
            return {"status": "failed", "stage": "planning", "error": str(e)}
        
        # Step 2: Database Generation
        print("\n🗄️  Step 2: Database Agent...")
        try:
            db_response = requests.post(
                f"{self.database_url}/agents/database",
                json={
                    "task_id": f"db_{story['id']}",
                    "story_id": story["id"],
                    "session_id": session_id,
                    "tables": architecture["database"]["tables"]
                },
                timeout=30
            )
            db_response.raise_for_status()
            db_result = db_response.json()
            print(f"✅ Generated {len(db_result['generated_files'])} database files")
        except Exception as e:
            print(f"❌ Database generation failed: {str(e)}")
        
        # Step 3: Backend Generation
        print("\n⚙️  Step 3: Backend Agent...")
        try:
            backend_response = requests.post(
                f"{self.backend_url}/agents/backend",
                json={
                    "task_id": f"backend_{story['id']}",
                    "story_id": story["id"],
                    "session_id": session_id,
                    "endpoints": architecture["backend"]["endpoints"]
                },
                timeout=30
            )
            backend_response.raise_for_status()
            backend_result = backend_response.json()
            print(f"✅ Generated {len(backend_result['generated_files'])} backend files")
        except Exception as e:
            print(f"❌ Backend generation failed: {str(e)}")
        
        # Step 4: Frontend Generation
        print("\n🎨 Step 4: Frontend Agent...")
        try:
            frontend_response = requests.post(
                f"{self.frontend_url}/agents/frontend",
                json={
                    "task_id": f"frontend_{story['id']}",
                    "story_id": story["id"],
                    "session_id": session_id,
                    "components": architecture["frontend"]["components"]
                },
                timeout=30
            )
            frontend_response.raise_for_status()
            frontend_result = frontend_response.json()
            print(f"✅ Generated {len(frontend_result['generated_files'])} frontend files")
        except Exception as e:
            print(f"❌ Frontend generation failed: {str(e)}")
        
        # Step 5: Testing
        print("\n🧪 Step 5: Testing Agent...")
        try:
            testing_response = requests.post(
                f"{self.testing_url}/agents/testing",
                json={
                    "task_id": f"testing_{story['id']}",
                    "story_id": story["id"],
                    "session_id": session_id,
                    "code_layers": ["database", "backend", "frontend"]
                },
                timeout=30
            )
            testing_response.raise_for_status()
            testing_result = testing_response.json()
            print(f"✅ Tests: {testing_result['total_tests']} total, Coverage: {testing_result['coverage']}%")
        except Exception as e:
            print(f"❌ Testing failed: {str(e)}")
        
        print("\n" + "=" * 60)
        print("✅ Story processing complete!")
        print("=" * 60)
        
        return {
            "status": "success",
            "story_id": story["id"],
            "session_id": session_id,
            "architecture": architecture
        }

# Example usage
if __name__ == "__main__":
    orchestrator = SimpleOrchestrator()
    
    # Sample user story
    sample_story = {
        "id": "US-001",
        "title": "User Authentication",
        "description": "As a user, I want to log in with email and password so that I can access my account",
        "acceptance_criteria": [
            {"id": 1, "text": "User can enter email and password", "priority": "must-have"},
            {"id": 2, "text": "System validates credentials", "priority": "must-have"},
            {"id": 3, "text": "User receives JWT token on success", "priority": "must-have"}
        ],
        "tech_hints": {
            "requires_auth": True,
            "requires_database": True,
            "requires_api": True,
            "requires_ui": True,
            "complexity": "medium"
        }
    }
    
    result = orchestrator.process_story(sample_story)
    
    print("\n📊 Final Result:")
    print(json.dumps(result, indent=2))
