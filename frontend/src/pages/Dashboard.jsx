import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { AlertCircle, Play, RotateCcw, Terminal, Check } from 'lucide-react';

export default function Dashboard() {
  const [findings, setFindings] = useState([]);
  const [loading, setLoading] = useState(false);
  const [activeAttack, setActiveAttack] = useState('duplicate_flood');
  const [explanations, setExplanations] = useState({});
  const [explainingId, setExplainingId] = useState(null);

  const fetchFindings = async () => {
    try {
      const res = await axios.get('http://localhost:8000/findings/');
      setFindings(res.data);
    } catch (err) {
      console.error("Error fetching findings", err);
    }
  };

  const runDemo = async (attackType = activeAttack) => {
    setLoading(true);
    try {
      await axios.post(`http://localhost:8000/demo/run?attack_type=${attackType}`);
      await fetchFindings();
    } catch (err) {
      console.error(err);
    }
    setLoading(false);
  };

  const resetPipeline = async () => {
    setLoading(true);
    try {
      await axios.post('http://localhost:8000/demo/reset');
      setFindings([]);
      setExplanations({});
    } catch (err) {
      console.error(err);
    }
    setLoading(false);
  };

  const fetchExplanation = async (findingId) => {
    if (explanations[findingId]) return;
    setExplainingId(findingId);
    try {
      const res = await axios.get(`http://localhost:8000/findings/${findingId}/explain`);
      setExplanations(prev => ({ ...prev, [findingId]: res.data.explanation }));
    } catch (err) {
      console.error("Error fetching AI explanation", err);
    }
    setExplainingId(null);
  };

  useEffect(() => {
    fetchFindings();
  }, []);

  return (
    <div className="space-y-6 max-w-5xl mx-auto">
      {/* Header & Controls */}
      <div className="flex flex-col md:flex-row md:items-end justify-between gap-4 pb-5 border-b border-[#212936]">
        <div>
          <h2 className="text-xl font-bold tracking-tight text-white">
            Assurance Findings
          </h2>
          <p className="text-slate-300 text-xs mt-1">
            Real-time adversary compromise detection across multi-contributor vision pipelines.
          </p>
        </div>

        {/* Action Controls */}
        <div className="flex flex-wrap items-center gap-2">
          <select 
            value={activeAttack}
            onChange={(e) => setActiveAttack(e.target.value)}
            className="bg-[#161c28] border border-[#2d3848] text-slate-100 text-xs rounded px-3 py-1.5 outline-none focus:border-white font-mono"
          >
            <option value="duplicate_flood">Attack: Duplicate Flood (DataGuard)</option>
            <option value="backdoor">Attack: Neural Backdoor (ModelShield)</option>
            <option value="drift">Attack: Sensor Drift (DriftLens)</option>
          </select>

          <button 
            onClick={() => runDemo(activeAttack)} 
            disabled={loading}
            className="flex items-center gap-1.5 bg-white hover:bg-slate-200 text-slate-950 px-3.5 py-1.5 rounded font-semibold text-xs transition-colors disabled:opacity-50"
          >
            <Play size={13} fill="currentColor" /> {loading ? 'Simulating...' : 'Simulate'}
          </button>

          <button 
            onClick={resetPipeline}
            disabled={loading}
            className="flex items-center gap-1.5 border border-[#2d3848] hover:border-slate-400 text-slate-200 hover:text-white bg-[#161c28] px-3 py-1.5 rounded text-xs transition-colors font-mono"
            title="Reset to clean baseline"
          >
            <RotateCcw size={13} /> Reset
          </button>
        </div>
      </div>

      {/* Structural Status Strip */}
      <div className="grid grid-cols-2 sm:grid-cols-4 border border-[#263143] rounded-md divide-x divide-[#263143] bg-[#141a24] text-xs font-mono">
        <div className="p-3.5">
          <span className="text-[11px] text-slate-400 font-medium uppercase block">Active Alerts</span>
          <span className={`font-bold text-sm mt-0.5 block ${findings.length > 0 ? 'text-rose-400' : 'text-slate-100'}`}>
            {findings.length} findings
          </span>
        </div>
        <div className="p-3.5">
          <span className="text-[11px] text-slate-400 font-medium uppercase block">Pipeline State</span>
          <span className={`font-bold text-sm mt-0.5 block ${findings.length > 0 ? 'text-rose-400' : 'text-emerald-400'}`}>
            {findings.length > 0 ? 'Quarantine Active' : 'Verified Secure'}
          </span>
        </div>
        <div className="p-3.5">
          <span className="text-[11px] text-slate-400 font-medium uppercase block">Canary Verification</span>
          <span className="font-bold text-sm text-emerald-400 mt-0.5 block">100% Passed</span>
        </div>
        <div className="p-3.5">
          <span className="text-[11px] text-slate-400 font-medium uppercase block">Assurance Protocol</span>
          <span className="font-bold text-sm text-slate-200 mt-0.5 block">ZTAAF Rule 1–5</span>
        </div>
      </div>

      {/* Findings List */}
      {findings.length === 0 ? (
        <div className="border border-dashed border-[#2d3848] bg-[#141a24]/50 rounded-md p-12 text-center">
          <Check size={28} className="mx-auto text-emerald-400 mb-2" />
          <h3 className="text-sm font-semibold text-slate-100">No Security Anomalies</h3>
          <p className="text-slate-300 text-xs max-w-sm mx-auto mt-1">
            Pipeline is operating within approved trust parameters. Use the control bar above to simulate adversary vectors.
          </p>
        </div>
      ) : (
        <div className="space-y-3.5">
          {findings.map((f, i) => {
            const isCritical = f.severity?.toLowerCase() === 'critical';
            const isHigh = f.severity?.toLowerCase() === 'high';
            const sevColorClass = isCritical 
              ? 'text-rose-300 bg-rose-950/70 border-rose-600' 
              : isHigh 
                ? 'text-amber-300 bg-amber-950/70 border-amber-600' 
                : 'text-yellow-200 bg-yellow-950/70 border-yellow-600';

            return (
              <div 
                key={f.finding_id || i} 
                className="border border-[#263143] bg-[#141a24] rounded-md p-5 space-y-4 hover:border-[#3b4b66] transition-colors"
              >
                <div className="flex flex-wrap items-center justify-between gap-2 border-b border-[#212936] pb-3">
                  <div className="flex items-center gap-2">
                    <AlertCircle size={16} className="text-rose-400" />
                    <span className="text-xs font-bold text-rose-400 tracking-wide font-mono">
                      {f.module.toUpperCase()} SECURITY FINDING
                    </span>
                    <span className="text-[11px] text-slate-400 font-mono">[{f.finding_id}]</span>
                  </div>
                  <div className="flex items-center gap-2 font-mono text-[10px]">
                    <span className={`px-2.5 py-0.5 rounded border uppercase font-bold ${sevColorClass}`}>
                      SEV: {f.severity}
                    </span>
                    <span className="px-2.5 py-0.5 rounded bg-rose-600 text-white font-bold uppercase tracking-wider">
                      ACTION: {f.recommended_action}
                    </span>
                  </div>
                </div>

                <div className="text-slate-200 text-xs leading-relaxed font-sans">
                  <span className="text-slate-400 font-semibold font-mono">Reason: </span>{f.reason}
                </div>

                {/* Data Table */}
                <div className="grid grid-cols-1 sm:grid-cols-3 gap-2.5 pt-1 text-xs font-mono">
                  <div className="border border-[#232d3d] bg-[#10141d] p-3 rounded">
                    <span className="text-[10px] text-slate-400 block uppercase font-medium">Affected Asset</span>
                    <span className="text-slate-100 font-semibold truncate block mt-0.5">{f.affected_asset.id}</span>
                  </div>

                  <div className="border border-[#232d3d] bg-[#10141d] p-3 rounded">
                    <span className="text-[10px] text-slate-400 block uppercase font-medium">Trust Propagation Drop</span>
                    <span className="text-rose-400 font-bold block mt-0.5">
                      {f.trust_score_before.toFixed(2)} → {f.trust_score_after.toFixed(2)} (-{((f.trust_score_before - f.trust_score_after) * 100).toFixed(0)}%)
                    </span>
                  </div>

                  <div className="border border-[#232d3d] bg-[#10141d] p-3 rounded">
                    <span className="text-[10px] text-slate-400 block uppercase font-medium">Confidence</span>
                    <span className="text-emerald-400 font-bold block mt-0.5">
                      {(f.confidence * 100).toFixed(0)}% (Canary Verified)
                    </span>
                  </div>
                </div>

                {/* Briefing Action */}
                <div className="pt-1">
                  {!explanations[f.finding_id] ? (
                    <button
                      onClick={() => fetchExplanation(f.finding_id)}
                      disabled={explainingId === f.finding_id}
                      className="flex items-center gap-1.5 text-xs font-mono border border-[#2d3848] hover:border-slate-300 text-slate-200 hover:text-white bg-[#161c28] px-3.5 py-1.5 rounded transition-colors"
                    >
                      <Terminal size={14} />
                      {explainingId === f.finding_id ? 'Synthesizing Tactical Briefing...' : 'Request Tactical AI Briefing'}
                    </button>
                  ) : (
                    <div className="border border-[#283446] bg-[#0f141d] p-4 rounded text-xs space-y-2">
                      <div className="text-[11px] font-bold text-slate-300 uppercase tracking-wider flex items-center gap-1.5 font-mono">
                        <Terminal size={13} className="text-slate-100" />
                        Tactical Commander Summary (Air-Gapped LLM)
                      </div>
                      <p className="text-slate-100 text-xs leading-relaxed font-sans">
                        {explanations[f.finding_id]}
                      </p>
                      <div className="text-[11px] text-slate-400 font-mono">
                        * Rule engine disposition is authoritative; summary is informational.
                      </div>
                    </div>
                  )}
                </div>
              </div>
          );
        })}
        </div>
      )}
    </div>
  );
}

