"""
Database Agent - Generates database schemas
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Database Agent")

class DatabaseTask(BaseModel):
    task_id: str
    story_id: str
    session_id: str
    tables: List[Dict]

class DatabaseResponse(BaseModel):
    status: str
    task_id: str
    generated_files: List[Dict[str, str]]

def generate_sql_schema(tables: List[Dict]) -> str:
    """Generate SQL schema"""
    
    sql = "-- Generated Database Schema\n\n"
    
    for table in tables:
        table_name = table.get("name", "table")
        columns = table.get("columns", [])
        
        sql += f"CREATE TABLE IF NOT EXISTS {table_name} (\n"
        
        column_defs = []
        for col in columns:
            col_def = f"    {col['name']} {col['type']}"
            if col.get("constraints"):
                col_def += f" {col['constraints']}"
            column_defs.append(col_def)
        
        sql += ",\n".join(column_defs)
        sql += "\n);\n\n"
        
        # Add indexes
        sql += f"CREATE INDEX IF NOT EXISTS idx_{table_name}_created ON {table_name}(created_at);\n\n"
    
    return sql

def generate_sqlalchemy_models(tables: List[Dict]) -> str:
    """Generate SQLAlchemy models"""
    
    code = """from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

"""
    
    for table in tables:
        table_name = table.get("name", "table")
        class_name = "".join([word.capitalize() for word in table_name.split("_")])
        
        code += f"class {class_name}(Base):\n"
        code += f"    __tablename__ = '{table_name}'\n\n"
        
        for col in table.get("columns", []):
            col_name = col["name"]
            col_type = col["type"]
            
            # Map SQL types to SQLAlchemy
            if "INT" in col_type or "SERIAL" in col_type:
                sa_type = "Integer"
            elif "VARCHAR" in col_type or "TEXT" in col_type:
                sa_type = "String"
            elif "TIMESTAMP" in col_type:
                sa_type = "DateTime"
            elif "BOOLEAN" in col_type:
                sa_type = "Boolean"
            else:
                sa_type = "String"
            
            constraints = col.get("constraints", "")
            primary_key = "PRIMARY KEY" in constraints
            
            code += f"    {col_name} = Column({sa_type}, primary_key={primary_key})\n"
        
        code += "\n"
    
    return code

@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "service": "database-agent",
        "timestamp": datetime.utcnow().isoformat()
    }

@app.post("/agents/database", response_model=DatabaseResponse)
async def generate_database(task: DatabaseTask):
    logger.info(f"Database generation for task: {task.task_id}")
    
    try:
        sql_schema = generate_sql_schema(task.tables)
        sqlalchemy_models = generate_sqlalchemy_models(task.tables)
        
        generated_files = [
            {
                "file_path": "database/schema.sql",
                "content": sql_schema,
                "language": "sql"
            },
            {
                "file_path": "app/models.py",
                "content": sqlalchemy_models,
                "language": "python"
            }
        ]
        
        logger.info(f"Generated database schema and models")
        
        return DatabaseResponse(
            status="success",
            task_id=task.task_id,
            generated_files=generated_files
        )
        
    except Exception as e:
        logger.error(f"Database generation failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8003)
