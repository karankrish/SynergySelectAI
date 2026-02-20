import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip as RechartsTooltip, Legend } from 'recharts';
import { User, CheckCircle, Zap, DollarSign, Activity } from 'lucide-react';

const COLORS = ['#3b82f6', '#8b5cf6', '#10b981', '#f59e0b', '#ef4444'];

export default function ResultsDashboard({ results }) {
    if (!results) return null;

    // Calculate seniority mix from candidates
    const roleCounts = results.Candidates.reduce((acc, c) => {
        acc[c.Role] = (acc[c.Role] || 0) + 1;
        return acc;
    }, {});

    const roleData = Object.entries(roleCounts).map(([name, value]) => ({
        name, value
    }));

    return (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '2rem' }}>
            {/* Top Value Cards */}
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))', gap: '1rem' }}>
                <div className="glass-panel" style={{ padding: '1rem' }}>
                    <h3><Zap size={18} style={{ display: 'inline', color: 'var(--accent-primary)', marginRight: '8px' }} />Synergy Index</h3>
                    <div style={{ fontSize: '2rem', fontWeight: 'bold', color: 'var(--text-primary)' }}>
                        {results.Synergy_Index}%
                    </div>
                </div>
                <div className="glass-panel" style={{ padding: '1rem' }}>
                    <h3><DollarSign size={18} style={{ display: 'inline', color: 'var(--success)', marginRight: '8px' }} />Total Cost</h3>
                    <div style={{ fontSize: '2rem', fontWeight: 'bold' }}>
                        ${results.Total_Cost.toLocaleString()}
                    </div>
                    <p style={{ fontSize: '0.85rem', color: 'var(--text-secondary)' }}>Remaining: ${results.Budget_Remaining.toLocaleString()}</p>
                </div>
                <div className="glass-panel" style={{ padding: '1rem' }}>
                    <h3><Activity size={18} style={{ display: 'inline', color: 'var(--warning)', marginRight: '8px' }} />Avg Performance</h3>
                    <div style={{ fontSize: '2rem', fontWeight: 'bold' }}>
                        {results.Avg_Performance} <span style={{ fontSize: '1rem', color: 'var(--text-secondary)' }}>/ 5.0</span>
                    </div>
                </div>
            </div>

            {/* Charts Section */}
            <div className="glass-panel" style={{ gridColumn: 'span 2' }}>
                <h3>Seniority Mix (1:2:3 Target)</h3>
                <div style={{ height: '300px' }}>
                    <ResponsiveContainer width="100%" height="100%">
                        <PieChart>
                            <Pie data={roleData} cx="50%" cy="50%" innerRadius={80} outerRadius={110} paddingAngle={5} dataKey="value">
                                {roleData.map((entry, index) => <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />)}
                            </Pie>
                            <RechartsTooltip />
                            <Legend />
                        </PieChart>
                    </ResponsiveContainer>
                </div>
            </div>
            <div className="glass-panel">
                <h3 style={{ marginBottom: '1.5rem' }}>Selected Team Roster ({results.Team_List})</h3>

                <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
                    {results.Candidates.map((c, i) => (
                        <div key={c.Employee_ID} style={{
                            background: 'rgba(15, 23, 42, 0.4)',
                            border: '1px solid var(--panel-border)',
                            borderRadius: '12px',
                            padding: '1rem',
                            display: 'flex',
                            gap: '1rem',
                            animationDelay: `${i * 0.05}s`
                        }} className="fade-in">
                            <div style={{
                                background: 'var(--panel-bg)',
                                borderRadius: '50%',
                                width: '48px',
                                height: '48px',
                                display: 'flex',
                                alignItems: 'center',
                                justifyContent: 'center',
                                flexShrink: 0
                            }}>
                                <User color="var(--text-secondary)" />
                            </div>

                            <div style={{ flex: 1 }}>
                                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.25rem' }}>
                                    <h4 style={{ margin: 0, color: 'var(--text-primary)' }}>
                                        Employee #{c.Employee_ID} <span style={{ color: 'var(--text-secondary)', fontWeight: 'normal', fontSize: '0.9rem' }}>- {c.Job_Title}</span>
                                    </h4>
                                    <div style={{ background: 'rgba(59, 130, 246, 0.2)', color: '#60a5fa', padding: '2px 8px', borderRadius: '12px', fontSize: '0.8rem', fontWeight: 600 }}>
                                        Score: {c.SynergyScore}
                                    </div>
                                </div>

                                <div style={{ display: 'flex', gap: '2rem', fontSize: '0.85rem', color: 'var(--text-secondary)', marginBottom: '0.75rem' }}>
                                    <span><strong>Role:</strong> {c.Role}</span>
                                    <span><strong>Cost:</strong> ${c.Salary.toLocaleString()}/mo</span>
                                </div>

                                <div style={{ fontSize: '0.9rem', color: 'var(--text-muted)', display: 'flex', gap: '0.5rem', alignItems: 'flex-start' }}>
                                    <CheckCircle size={14} color="var(--success)" style={{ marginTop: '3px', flexShrink: 0 }} />
                                    <span>{c.Explainability}</span>
                                </div>
                            </div>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
}
