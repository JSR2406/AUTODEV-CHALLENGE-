-- AutoDev Platform Database Schema

CREATE TABLE IF NOT EXISTS execution_logs (
    id SERIAL PRIMARY KEY,
    story_id VARCHAR(100) NOT NULL,
    agent_name VARCHAR(50) NOT NULL,
    status VARCHAR(20) NOT NULL,
    output JSONB,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS generated_code (
    id SERIAL PRIMARY KEY,
    story_id VARCHAR(100) NOT NULL,
    session_id VARCHAR(200),
    layer VARCHAR(20) NOT NULL,
    file_path TEXT NOT NULL,
    content TEXT NOT NULL,
    language VARCHAR(20),
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS test_results (
    id SERIAL PRIMARY KEY,
    story_id VARCHAR(100) NOT NULL,
    test_type VARCHAR(50),
    passed BOOLEAN,
    coverage_percentage DECIMAL(5,2),
    total_tests INTEGER,
    failed_tests INTEGER,
    test_output JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS agent_metrics (
    id SERIAL PRIMARY KEY,
    agent_name VARCHAR(50) NOT NULL,
    task_id VARCHAR(200),
    execution_time_seconds INTEGER,
    tokens_used INTEGER,
    success BOOLEAN,
    error_message TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_execution_logs_story ON execution_logs(story_id);
CREATE INDEX IF NOT EXISTS idx_execution_logs_agent ON execution_logs(agent_name);
CREATE INDEX IF NOT EXISTS idx_generated_code_story ON generated_code(story_id);
CREATE INDEX IF NOT EXISTS idx_test_results_story ON test_results(story_id);
CREATE INDEX IF NOT EXISTS idx_agent_metrics_agent ON agent_metrics(agent_name);

GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO postgres;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO postgres;
