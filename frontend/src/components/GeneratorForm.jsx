import { useState } from 'react';
import { Loader2, Users, DollarSign, Building } from 'lucide-react';

export default function GeneratorForm({ onSubmit, loading }) {
    const [department, setDepartment] = useState('Engineering');
    const [teamSize, setTeamSize] = useState(12);
    const [budget, setBudget] = useState(100000);

    const handleSubmit = (e) => {
        e.preventDefault();
        onSubmit({
            department,
            team_size: parseInt(teamSize, 10),
            total_budget: parseFloat(budget)
        });
    };

    const departments = ['Engineering', 'Sales', 'Marketing', 'Customer Support', 'Finance', 'HR', 'Legal', 'Operations', 'IT'];

    return (
        <div className="glass-panel">
            <h2>Team Parameters</h2>
            <form onSubmit={handleSubmit}>
                <div className="form-group">
                    <label><Building size={16} style={{ display: 'inline', verticalAlign: 'text-bottom', marginRight: '4px' }} /> Department</label>
                    <select
                        className="form-control"
                        value={department}
                        onChange={(e) => setDepartment(e.target.value)}
                    >
                        {departments.map(d => (
                            <option key={d} value={d}>{d}</option>
                        ))}
                    </select>
                </div>

                <div className="form-group">
                    <label><Users size={16} style={{ display: 'inline', verticalAlign: 'text-bottom', marginRight: '4px' }} /> Team Size ({teamSize})</label>
                    <input
                        type="range"
                        min="3"
                        max="30"
                        className="form-control"
                        style={{ padding: 0 }}
                        value={teamSize}
                        onChange={(e) => setTeamSize(e.target.value)}
                    />
                </div>

                <div className="form-group">
                    <label><DollarSign size={16} style={{ display: 'inline', verticalAlign: 'text-bottom', marginRight: '4px' }} /> Total Budget ($)</label>
                    <input
                        type="number"
                        className="form-control"
                        min="10000"
                        max="1000000"
                        step="1000"
                        value={budget}
                        onChange={(e) => setBudget(e.target.value)}
                    />
                </div>

                <button type="submit" className="btn-primary" disabled={loading} style={{ marginTop: '1rem' }}>
                    {loading ? <Loader2 className="animate-spin" /> : 'Generate Team'}
                </button>
            </form>
        </div>
    );
}
