import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { AlertTriangle, Play } from 'lucide-react';

export default function Dashboard() {
  const [findings, setFindings] = useState([]);
  const [loading, setLoading] = useState(false);

  const fetchFindings = async () => {
    try {
      const res = await axios.get('http://localhost:8000/findings/');
      setFindings(res.data);
    } catch (err) {
      console.error("Error fetching findings", err);
    }
  };

  const runDemo = async () => {
    setLoading(true);
    try {
      await axios.post('http://localhost:8000/demo/run');
      await fetchFindings();
    } catch (err) {
      console.error(err);
    }
    setLoading(false);
  };

  useEffect(() => {
    fetchFindings();
  }, []);

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h2 className="text-3xl font-bold bg-gradient-to-r from-primary to-accent bg-clip-text text-transparent">
          Assurance Findings
        </h2>
        <button 
          onClick={runDemo} 
          disabled={loading}
          className="flex items-center gap-2 bg-primary hover:bg-blue-600 text-white px-4 py-2 rounded-lg transition"
        >
          <Play size={18} /> {loading ? 'Running...' : 'Run ZTAAF Demo'}
        </button>
      </div>

      {findings.length === 0 ? (
        <div className="bg-dark p-8 rounded-xl border border-slate-800 text-center text-slate-500">
          No findings yet. Run the demo pipeline to generate data.
        </div>
      ) : (
        <div className="grid gap-4">
          {findings.map((f, i) => (
            <div key={i} className="bg-dark p-6 rounded-xl border border-slate-800 flex flex-col gap-3 shadow-lg hover:border-slate-600 transition">
              <div className="flex justify-between">
                <span className="flex items-center gap-2 text-danger font-semibold">
                  <AlertTriangle size={20} /> {f.module} Alert
                </span>
                <span className="text-sm bg-slate-800 px-3 py-1 rounded-full">{f.severity.toUpperCase()}</span>
              </div>
              <p className="text-slate-300">{f.reason}</p>
              <div className="grid grid-cols-2 gap-4 mt-2">
                <div className="bg-slate-900 p-3 rounded-lg text-sm">
                  <span className="text-slate-500 block">Affected Asset</span>
                  <span className="font-mono text-primary">{f.affected_asset.id}</span>
                </div>
                <div className="bg-slate-900 p-3 rounded-lg text-sm">
                  <span className="text-slate-500 block">Trust Drop</span>
                  <span className="font-mono text-danger">
                    {f.trust_score_before.toFixed(2)} → {f.trust_score_after.toFixed(2)}
                  </span>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
