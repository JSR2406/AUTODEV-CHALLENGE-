import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

const API_BASE = 'http://localhost:8000';

function App() {
    const [agents, setAgents] = useState([
        { name: 'Planning', port: 8000, status: 'unknown', color: '#3b82f6', icon: '🧠' },
        { name: 'Frontend', port: 8001, status: 'unknown', color: '#8b5cf6', icon: '🎨' },
        { name: 'Backend', port: 8002, status: 'unknown', color: '#10b981', icon: '⚙️' },
        { name: 'Database', port: 8003, status: 'unknown', color: '#f59e0b', icon: '🗄️' },
        { name: 'Testing', port: 8004, status: 'unknown', color: '#ef4444', icon: '🧪' },
    ]);

    const [logs, setLogs] = useState([]);
    const [storyInput, setStoryInput] = useState({
        title: 'User Authentication',
        description: 'As a user, I want to log in with email and password',
        criteria: 'User can enter credentials\nSystem validates credentials\nJWT token returned'
    });
    const [processing, setProcessing] = useState(false);
    const [result, setResult] = useState(null);
    const [isLoading, setIsLoading] = useState(true);
    const [progress, setProgress] = useState(0);

    // Check agent health
    useEffect(() => {
        const checkHealth = async () => {
            const updatedAgents = await Promise.all(
                agents.map(async (agent) => {
                    try {
                        const response = await axios.get(`http://localhost:${agent.port}/health`, {
                            timeout: 2000
                        });
                        return { ...agent, status: response.data.status === 'healthy' ? 'healthy' : 'unhealthy' };
                    } catch (error) {
                        return { ...agent, status: 'offline' };
                    }
                })
            );
            setAgents(updatedAgents);
            setIsLoading(false);
        };

        checkHealth();
        const interval = setInterval(checkHealth, 10000); // Check every 10s

        return () => clearInterval(interval);
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, []);

    const addLog = (message, type = 'info') => {
        const timestamp = new Date().toLocaleTimeString();
        setLogs(prev => [{ timestamp, message, type }, ...prev].slice(0, 50));
    };

    const processStory = async () => {
        setProcessing(true);
        setResult(null);
        setProgress(0);
        addLog('🚀 Starting story processing...', 'info');

        try {
            // Step 1: Planning (20% progress)
            setProgress(10);
            addLog('📋 Calling Planning Agent...', 'info');

            const planningResponse = await axios.post(`${API_BASE}/agents/planning`, {
                story_id: `US-${Date.now()}`,
                session_id: `session_${Date.now()}`,
                title: storyInput.title,
                description: storyInput.description,
                acceptance_criteria: storyInput.criteria.split('\n').map((text, idx) => ({
                    id: idx + 1,
                    text: text.trim(),
                    priority: 'must-have'
                })),
                tech_hints: {
                    requires_auth: true,
                    requires_database: true,
                    requires_api: true,
                    requires_ui: true,
                    complexity: 'medium'
                },
                project_id: 'demo-project'
            });

            setProgress(20);
            addLog(`✅ Planning completed (${planningResponse.data.execution_time_seconds.toFixed(2)}s)`, 'success');

            const architecture = planningResponse.data.architecture;

            // Step 2: Database (40% progress)
            setProgress(30);
            addLog('🗄️  Calling Database Agent...', 'info');
            const dbResponse = await axios.post('http://localhost:8003/agents/database', {
                task_id: `db_${Date.now()}`,
                story_id: planningResponse.data.story_id,
                session_id: planningResponse.data.session_id,
                tables: architecture.database.tables
            });
            setProgress(40);
            addLog(`✅ Generated ${dbResponse.data.generated_files.length} database files`, 'success');

            // Step 3: Backend (60% progress)
            setProgress(50);
            addLog('⚙️  Calling Backend Agent...', 'info');
            const backendResponse = await axios.post('http://localhost:8002/agents/backend', {
                task_id: `backend_${Date.now()}`,
                story_id: planningResponse.data.story_id,
                session_id: planningResponse.data.session_id,
                endpoints: architecture.backend.endpoints
            });
            setProgress(60);
            addLog(`✅ Generated ${backendResponse.data.generated_files.length} backend files`, 'success');

            // Step 4: Frontend (80% progress)
            setProgress(70);
            addLog('🎨 Calling Frontend Agent...', 'info');
            const frontendResponse = await axios.post('http://localhost:8001/agents/frontend', {
                task_id: `frontend_${Date.now()}`,
                story_id: planningResponse.data.story_id,
                session_id: planningResponse.data.session_id,
                components: architecture.frontend.components
            });
            setProgress(80);
            addLog(`✅ Generated ${frontendResponse.data.generated_files.length} frontend files`, 'success');

            // Step 5: Testing (100% progress)
            setProgress(90);
            addLog('🧪 Calling Testing Agent...', 'info');
            const testingResponse = await axios.post('http://localhost:8004/agents/testing', {
                task_id: `testing_${Date.now()}`,
                story_id: planningResponse.data.story_id,
                session_id: planningResponse.data.session_id,
                code_layers: ['database', 'backend', 'frontend']
            });
            setProgress(100);
            addLog(`✅ Tests: ${testingResponse.data.total_tests} total, Coverage: ${testingResponse.data.coverage}%`, 'success');

            setResult({
                architecture,
                database: dbResponse.data,
                backend: backendResponse.data,
                frontend: frontendResponse.data,
                testing: testingResponse.data
            });

            addLog('🎉 Story processing complete!', 'success');

        } catch (error) {
            addLog(`❌ Error: ${error.message}`, 'error');
            console.error('Processing error:', error);
            setProgress(0);
        } finally {
            setProcessing(false);
        }
    };

    // Skeleton loader component
    const SkeletonCard = () => (
        <div className="agent-card">
            <div className="skeleton" style={{ height: '20px', width: '60%', marginBottom: '10px' }}></div>
            <div className="skeleton" style={{ height: '16px', width: '40%', marginBottom: '8px' }}></div>
            <div className="skeleton" style={{ height: '14px', width: '50%' }}></div>
        </div>
    );

    return (
        <div className="App">
            <header className="header">
                <h1>🚀 AutoDev Platform - Multi-Agent Dashboard</h1>
                <p>Collaborative Agentic Platform for Full-Stack Development</p>
            </header>

            <div className="container">
                {/* Agent Status Grid */}
                <section className="agent-status">
                    <h2>Agent Status</h2>
                    <div className="agent-grid">
                        {isLoading ? (
                            // Show skeleton loaders while loading
                            Array(5).fill(0).map((_, idx) => <SkeletonCard key={idx} />)
                        ) : (
                            agents.map(agent => (
                                <div key={agent.name} className={`agent-card ${agent.status}`}>
                                    <div className="agent-header" style={{ borderLeftColor: agent.color }}>
                                        <h3>{agent.icon} {agent.name} Agent</h3>
                                        <span className={`status-badge ${agent.status}`}>
                                            {agent.status === 'healthy' ? '✅' : agent.status === 'offline' ? '🔴' : '⚠️'}
                                        </span>
                                    </div>
                                    <p className="agent-port">Port: {agent.port}</p>
                                    <a
                                        href={`http://localhost:${agent.port}/docs`}
                                        target="_blank"
                                        rel="noopener noreferrer"
                                        className="api-docs-link"
                                    >
                                        API Docs →
                                    </a>
                                </div>
                            ))
                        )}
                    </div>
                </section>

                {/* Story Input Form */}
                <section className="story-input">
                    <h2>Process User Story</h2>

                    {/* Progress Bar */}
                    {processing && (
                        <div style={{
                            marginBottom: '1.5rem',
                            background: 'rgba(255, 255, 255, 0.1)',
                            borderRadius: '8px',
                            overflow: 'hidden',
                            height: '8px'
                        }}>
                            <div style={{
                                height: '100%',
                                width: `${progress}%`,
                                background: 'linear-gradient(90deg, #4facfe 0%, #00f2fe 100%)',
                                transition: 'width 0.5s ease',
                                boxShadow: '0 0 10px rgba(79, 172, 254, 0.5)'
                            }}></div>
                        </div>
                    )}

                    <div className="form-group">
                        <label>Story Title</label>
                        <input
                            type="text"
                            value={storyInput.title}
                            onChange={(e) => setStoryInput({ ...storyInput, title: e.target.value })}
                            placeholder="E.g., User Authentication"
                            disabled={processing}
                        />
                    </div>

                    <div className="form-group">
                        <label>Description</label>
                        <textarea
                            value={storyInput.description}
                            onChange={(e) => setStoryInput({ ...storyInput, description: e.target.value })}
                            placeholder="As a user, I want to..."
                            rows={3}
                            disabled={processing}
                        />
                    </div>

                    <div className="form-group">
                        <label>Acceptance Criteria (one per line)</label>
                        <textarea
                            value={storyInput.criteria}
                            onChange={(e) => setStoryInput({ ...storyInput, criteria: e.target.value })}
                            placeholder="Criterion 1\nCriterion 2\nCriterion 3"
                            rows={4}
                            disabled={processing}
                        />
                    </div>

                    <button
                        onClick={processStory}
                        disabled={processing}
                        className="process-button"
                    >
                        {processing ? `⏳ Processing... ${progress}%` : '🚀 Process Story'}
                    </button>
                </section>

                {/* Live Logs */}
                <section className="logs-section">
                    <h2>Live Execution Log</h2>
                    <div className="logs-container">
                        {logs.length === 0 ? (
                            <p className="no-logs">No logs yet. Process a story to see activity.</p>
                        ) : (
                            logs.map((log, idx) => (
                                <div key={idx} className={`log-entry ${log.type}`}>
                                    <span className="log-time">{log.timestamp}</span>
                                    <span className="log-message">{log.message}</span>
                                </div>
                            ))
                        )}
                    </div>
                </section>

                {/* Results Display */}
                {result && (
                    <section className="results-section">
                        <h2>Generation Results</h2>

                        <div className="result-card">
                            <h3>🗄️ Database Schema</h3>
                            <p><strong>Tables:</strong> {result.architecture.database.tables.length}</p>
                            <ul>
                                {result.architecture.database.tables.map((table, idx) => (
                                    <li key={idx}>{table.name} ({table.columns.length} columns)</li>
                                ))}
                            </ul>
                        </div>

                        <div className="result-card">
                            <h3>⚙️ Backend API</h3>
                            <p><strong>Endpoints:</strong> {result.architecture.backend.endpoints.length}</p>
                            <ul>
                                {result.architecture.backend.endpoints.map((ep, idx) => (
                                    <li key={idx}>
                                        <span className="http-method">{ep.method}</span> {ep.path}
                                    </li>
                                ))}
                            </ul>
                        </div>

                        <div className="result-card">
                            <h3>🎨 Frontend Components</h3>
                            <p><strong>Components:</strong> {result.architecture.frontend.components.length}</p>
                            <ul>
                                {result.architecture.frontend.components.map((comp, idx) => (
                                    <li key={idx}>{comp}</li>
                                ))}
                            </ul>
                        </div>

                        <div className="result-card">
                            <h3>🧪 Test Results</h3>
                            <p><strong>Total Tests:</strong> {result.testing.total_tests}</p>
                            <p><strong>Coverage:</strong> {result.testing.coverage}%</p>
                            <p><strong>Status:</strong> {result.testing.tests_passed ? '✅ All Passed' : '❌ Some Failed'}</p>
                        </div>
                    </section>
                )}
            </div>
        </div>
    );
}

export default App;
