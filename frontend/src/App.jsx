import { useState } from 'react';
import GeneratorForm from './components/GeneratorForm';
import ResultsDashboard from './components/ResultsDashboard';
import './index.css';

function App() {
    const [results, setResults] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    const generateTeam = async (params) => {
        setLoading(true);
        setError(null);
        setResults(null);
        try {
            const res = await fetch('/api/v1/team/generate', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(params)
            });
            const data = await res.json();
            if (!res.ok) throw new Error(data.detail || 'Failed to generate team');
            setResults(data);
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="app-container">
            <header className="app-header fade-in">
                <h1>SynergySelect AI</h1>
                <p>Intelligent Team-as-a-Service Engine</p>
            </header>

            <main className="fade-in" style={{ animationDelay: '0.1s' }}>
                <div style={{ display: 'grid', gridTemplateColumns: results ? '1fr 2fr' : '1fr', gap: '2rem', transition: 'all 0.5s ease' }}>
                    <div>
                        <GeneratorForm onSubmit={generateTeam} loading={loading} />
                    </div>

                    <div style={{ display: 'flex', flexDirection: 'column', gap: '2rem' }}>
                        {error && (
                            <div className="error-card fade-in">
                                {error}
                            </div>
                        )}

                        {results && (
                            <ResultsDashboard results={results} />
                        )}
                    </div>
                </div>
            </main>
        </div>
    );
}

export default App;
