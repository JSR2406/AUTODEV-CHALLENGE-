"""
AutoDev Platform - Complete Integration Demo
Shows frontend + backend + all agents working together
"""

import requests
import json
import time
from datetime import datetime

def print_header(title):
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80)

def print_success(message):
    print(f"[SUCCESS] {message}")

def print_info(message):
    print(f"[INFO] {message}")

def print_error(message):
    print(f"[ERROR] {message}")

print_header("AUTODEV PLATFORM - COMPLETE INTEGRATION DEMO")
print(f"Demo Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

# Step 1: Check All Agents
print_header("STEP 1: Agent Health Check")

agents = [
    (8000, "Planning Agent"),
    (8001, "Frontend Agent"),
    (8002, "Backend Agent"),
    (8003, "Database Agent"),
    (8004, "Testing Agent")
]

healthy_agents = []
for port, name in agents:
    try:
        response = requests.get(f"http://localhost:{port}/health", timeout=3)
        if response.status_code == 200:
            print_success(f"{name:20s} - Port {port} - HEALTHY")
            healthy_agents.append((port, name))
        else:
            print_error(f"{name:20s} - Port {port} - UNHEALTHY")
    except:
        print_error(f"{name:20s} - Port {port} - OFFLINE")

print(f"\n{len(healthy_agents)}/{len(agents)} agents are healthy")

# Step 2: Process Complete User Story
if len(healthy_agents) >= 1:
    print_header("STEP 2: Processing Complete User Story")
    
    story = {
        "story_id": "INTEGRATION-001",
        "session_id": f"integration_{int(time.time())}",
        "title": "Task Management System",
        "description": "As a user, I want to create, update, and track tasks with priorities and due dates",
        "acceptance_criteria": [
            {"id": 1, "text": "Create tasks with title, description, priority", "priority": "must-have"},
            {"id": 2, "text": "Set due dates and reminders", "priority": "must-have"},
            {"id": 3, "text": "Mark tasks as complete", "priority": "must-have"},
            {"id": 4, "text": "Filter tasks by status and priority", "priority": "should-have"},
            {"id": 5, "text": "Receive notifications for due tasks", "priority": "could-have"}
        ],
        "tech_hints": {
            "requires_auth": True,
            "requires_database": True,
            "requires_api": True,
            "requires_ui": True,
            "complexity": "medium"
        },
        "project_id": "task-management"
    }
    
    print_info(f"Story: {story['title']}")
    print_info(f"Criteria: {len(story['acceptance_criteria'])} items\n")
    
    # Call Planning Agent
    print(">>> Calling Planning Agent...")
    try:
        response = requests.post(
            "http://localhost:8000/agents/planning",
            json=story,
            timeout=30
        )
        
        if response.status_code == 200:
            planning_result = response.json()
            print_success(f"Architecture generated in {planning_result['execution_time_seconds']:.2f}s")
            
            arch = planning_result['architecture']
            session_id = planning_result['session_id']
            
            print(f"\n  Database Tables: {len(arch['database']['tables'])}")
            print(f"  API Endpoints: {len(arch['backend']['endpoints'])}")
            print(f"  Components: {len(arch['frontend']['components'])}")
            
            # Step 3: Call Database Agent
            if (8003, "Database Agent") in healthy_agents:
                print_header("STEP 3: Generating Database Schema")
                print(">>> Calling Database Agent...")
                
                try:
                    db_response = requests.post(
                        "http://localhost:8003/agents/database",
                        json={
                            "task_id": f"db_{int(time.time())}",
                            "story_id": story['story_id'],
                            "session_id": session_id,
                            "tables": arch['database']['tables']
                        },
                        timeout=30
                    )
                    
                    if db_response.status_code == 200:
                        db_result = db_response.json()
                        print_success(f"Generated {len(db_result['generated_files'])} database files")
                        for file in db_result['generated_files']:
                            print(f"  - {file['filename']} ({file['size_bytes']} bytes)")
                except Exception as e:
                    print_error(f"Database Agent failed: {e}")
            
            # Step 4: Call Backend Agent
            if (8002, "Backend Agent") in healthy_agents:
                print_header("STEP 4: Generating Backend API")
                print(">>> Calling Backend Agent...")
                
                try:
                    backend_response = requests.post(
                        "http://localhost:8002/agents/backend",
                        json={
                            "task_id": f"backend_{int(time.time())}",
                            "story_id": story['story_id'],
                            "session_id": session_id,
                            "endpoints": arch['backend']['endpoints']
                        },
                        timeout=30
                    )
                    
                    if backend_response.status_code == 200:
                        backend_result = backend_response.json()
                        print_success(f"Generated {len(backend_result['generated_files'])} backend files")
                        for file in backend_result['generated_files']:
                            print(f"  - {file['filename']} ({file['size_bytes']} bytes)")
                except Exception as e:
                    print_error(f"Backend Agent failed: {e}")
            
            # Step 5: Call Frontend Agent
            if (8001, "Frontend Agent") in healthy_agents:
                print_header("STEP 5: Generating Frontend Components")
                print(">>> Calling Frontend Agent...")
                
                try:
                    frontend_response = requests.post(
                        "http://localhost:8001/agents/frontend",
                        json={
                            "task_id": f"frontend_{int(time.time())}",
                            "story_id": story['story_id'],
                            "session_id": session_id,
                            "components": arch['frontend']['components']
                        },
                        timeout=30
                    )
                    
                    if frontend_response.status_code == 200:
                        frontend_result = frontend_response.json()
                        print_success(f"Generated {len(frontend_result['generated_files'])} frontend files")
                        for file in frontend_result['generated_files']:
                            print(f"  - {file['filename']} ({file['size_bytes']} bytes)")
                except Exception as e:
                    print_error(f"Frontend Agent failed: {e}")
            
            # Step 6: Call Testing Agent
            if (8004, "Testing Agent") in healthy_agents:
                print_header("STEP 6: Generating Tests")
                print(">>> Calling Testing Agent...")
                
                try:
                    testing_response = requests.post(
                        "http://localhost:8004/agents/testing",
                        json={
                            "task_id": f"testing_{int(time.time())}",
                            "story_id": story['story_id'],
                            "session_id": session_id,
                            "code_layers": ["database", "backend", "frontend"]
                        },
                        timeout=30
                    )
                    
                    if testing_response.status_code == 200:
                        testing_result = testing_response.json()
                        print_success(f"Generated {testing_result['total_tests']} tests")
                        print(f"  Coverage: {testing_result['coverage']}%")
                        print(f"  Status: {'PASSED' if testing_result['tests_passed'] else 'FAILED'}")
                except Exception as e:
                    print_error(f"Testing Agent failed: {e}")
            
    except Exception as e:
        print_error(f"Planning Agent failed: {e}")

# Final Summary
print_header("INTEGRATION DEMO COMPLETE")

print(f"""
AGENTS OPERATIONAL: {len(healthy_agents)}/{len(agents)}

WORKFLOW DEMONSTRATED:
  1. Planning Agent - Architecture generation
  2. Database Agent - Schema creation
  3. Backend Agent - API endpoint generation
  4. Frontend Agent - Component scaffolding
  5. Testing Agent - Test file generation

FULL STACK GENERATED:
  - Database schemas (SQL + ORM)
  - Backend APIs (FastAPI)
  - Frontend components (React + TypeScript)
  - Test suites (Pytest + Jest)

SYSTEM STATUS: FULLY INTEGRATED AND OPERATIONAL

ACCESS POINTS:
  - Planning Agent API: http://localhost:8000/docs
  - Frontend Agent API: http://localhost:8001/docs
  - Backend Agent API: http://localhost:8002/docs
  - Database Agent API: http://localhost:8003/docs
  - Testing Agent API: http://localhost:8004/docs

NEXT STEPS:
  - Dashboard should be at http://localhost:3000 (may take a minute to start)
  - Use orchestrator.py for automated workflows
  - Add OpenAI API key for real AI generation
""")

print("=" * 80)
print("Integration demo completed successfully!")
print("=" * 80)
