import React, { useEffect, useState } from 'react';
import axios from 'axios';
import ReactFlow, { Background, Controls } from 'reactflow';
import 'reactflow/dist/style.css';
import { Play, RotateCcw } from 'lucide-react';

export default function TrustGraphView() {
  const [nodes, setNodes] = useState([]);
  const [edges, setEdges] = useState([]);
  const [loading, setLoading] = useState(false);
  const [attackType, setAttackType] = useState('duplicate_flood');

  const fetchGraph = async () => {
    try {
      const nodeRes = await axios.get('http://localhost:8000/graph/nodes');
      const edgeRes = await axios.get('http://localhost:8000/graph/propagation-history');

      const typeOrder = {
        'contributor': 0,
        'dataset_batch': 1,
        'model': 2,
        'inference_service': 3
      };

      const formattedNodes = nodeRes.data.map((n, i) => {
        const orderIdx = typeOrder[n.node_type] !== undefined ? typeOrder[n.node_type] : (i % 4);
        const posX = 40 + orderIdx * 260;
        const posY = 150 + (i >= 4 ? Math.floor(i / 4) * 160 : 0);

        const isTrusted = n.trust_score >= 0.70;
        const isCaution = n.trust_score >= 0.40 && n.trust_score < 0.70;
        const isQuarantined = n.trust_score < 0.40;
        const isLocked = n.crypto_locked;

        let badgeBg = '#052e16';
        let badgeBorder = '#166534';
        let badgeText = '#4ade80';
        let badgeLabel = 'VERIFIED';
        let cardBg = '#0d2218';
        let cardBorder = '#166534';
        let barColor = '#22c55e';

        if (isLocked) {
          badgeBg = '#450a0a';
          badgeBorder = '#991b1b';
          badgeText = '#fca5a5';
          badgeLabel = 'LOCKED';
          cardBg = '#360910';
          cardBorder = '#dc2626';
          barColor = '#f87171';
        } else if (isQuarantined) {
          badgeBg = '#450a0a';
          badgeBorder = '#7f1d1d';
          badgeText = '#f87171';
          badgeLabel = 'QUARANTINED';
          cardBg = '#260a0f';
          cardBorder = '#b91c1c';
          barColor = '#ef4444';
        } else if (isCaution) {
          badgeBg = '#451a03';
          badgeBorder = '#92400e';
          badgeText = '#fcd34d';
          badgeLabel = 'SUSPICIOUS';
          cardBg = '#231805';
          cardBorder = '#b45309';
          barColor = '#f59e0b';
        }

        return {
          id: n.node_id,
          position: { x: posX, y: posY },
          data: { 
            label: (
              <div className="p-3 text-left font-mono">
                <div className="flex items-center justify-between gap-1 mb-1.5 pb-1.5 border-b border-[#2d3748]">
                  <span className="text-[9px] uppercase tracking-wider text-slate-300 font-bold">
                    {n.node_type.replace('_', ' ')}
                  </span>
                  <span 
                    className="text-[9px] font-bold px-1.5 py-0.5 rounded uppercase"
                    style={{ backgroundColor: badgeBg, borderColor: badgeBorder, color: badgeText, borderWidth: '1px' }}
                  >
                    {badgeLabel}
                  </span>
                </div>
                
                <div className="text-[12px] font-bold text-white truncate">
                  {n.node_id}
                </div>

                <div className="mt-2.5 flex items-center justify-between text-[11px]">
                  <span className="text-slate-300 font-medium">Trust Score:</span>
                  <span className="font-bold text-sm" style={{ color: barColor }}>
                    {n.trust_score.toFixed(2)}
                  </span>
                </div>

                <div className="w-full bg-[#1e2636] h-1.5 mt-1.5 overflow-hidden rounded-full">
                  <div 
                    className="h-full transition-all duration-300" 
                    style={{ width: `${Math.max(4, n.trust_score * 100)}%`, backgroundColor: barColor }}
                  />
                </div>
              </div>
            ) 
          },
          style: {
            background: cardBg,
            border: `1.5px solid ${cardBorder}`,
            borderRadius: '8px',
            width: 220,
            boxShadow: 'none'
          }
        };
      });

      const formattedEdges = edgeRes.data.edges.map((e, i) => {
        // Highlight edge if distrust has propagated through it
        const sourceNode = nodeRes.data.find(n => n.node_id === e.source);
        const targetNode = nodeRes.data.find(n => n.node_id === e.target);
        const isDistrustedEdge = (sourceNode && sourceNode.trust_score < 0.5) || (targetNode && targetNode.trust_score < 0.5);

        return {
          id: `e-${e.source}-${e.target}-${i}`,
          source: e.source,
          target: e.target,
          animated: true,
          style: { 
            stroke: isDistrustedEdge ? '#ef4444' : '#22c55e', 
            strokeWidth: isDistrustedEdge ? 2.5 : 1.8 
          }
        };
      });

      setNodes(formattedNodes);
      setEdges(formattedEdges);
    } catch (err) {
      console.error(err);
    }
  };

  const runAttack = async (type = attackType) => {
    setLoading(true);
    try {
      await axios.post(`http://localhost:8000/demo/run?attack_type=${type}`);
      await fetchGraph();
    } catch (err) {
      console.error(err);
    }
    setLoading(false);
  };

  const resetGraph = async () => {
    setLoading(true);
    try {
      await axios.post('http://localhost:8000/demo/reset');
      await fetchGraph();
    } catch (err) {
      console.error(err);
    }
    setLoading(false);
  };

  useEffect(() => {
    fetchGraph();
  }, []);

  return (
    <div className="h-full flex flex-col space-y-4 max-w-6xl mx-auto">
      {/* Header & Controls */}
      <div className="flex flex-col md:flex-row md:items-end justify-between gap-4 pb-4 border-b border-[#212936]">
        <div>
          <h2 className="text-xl font-bold tracking-tight text-white">
            Trust Propagation Graph
          </h2>
          <p className="text-slate-300 text-xs mt-1">
            ZTAAF Rule 3: Upstream compromise cascades 50% distrust penalty to dependent downstream nodes.
          </p>
        </div>

        <div className="flex flex-wrap items-center gap-2">
          <select 
            value={attackType}
            onChange={(e) => setAttackType(e.target.value)}
            className="bg-[#161c28] border border-[#2d3848] text-slate-100 text-xs rounded px-3 py-1.5 outline-none focus:border-white font-mono"
          >
            <option value="duplicate_flood">Attack: Duplicate Flood (DataGuard)</option>
            <option value="backdoor">Attack: Backdoor Injection (ModelShield)</option>
            <option value="drift">Attack: Sensor Drift (DriftLens)</option>
          </select>

          <button 
            onClick={() => runAttack(attackType)} 
            disabled={loading}
            className="flex items-center gap-1.5 bg-white hover:bg-slate-200 text-slate-950 px-3.5 py-1.5 rounded font-semibold text-xs transition-colors disabled:opacity-50"
          >
            <Play size={13} fill="currentColor" /> {loading ? 'Propagating...' : 'Trigger Attack'}
          </button>

          <button 
            onClick={resetGraph}
            disabled={loading}
            className="flex items-center gap-1.5 border border-[#2d3848] hover:border-slate-300 text-slate-200 hover:text-white bg-[#161c28] px-3 py-1.5 rounded text-xs transition-colors font-mono"
          >
            <RotateCcw size={13} /> Reset
          </button>
        </div>
      </div>
      
      {/* Graph Canvas */}
      <div className="flex-1 bg-[#0c1017] border border-[#263143] rounded-md overflow-hidden min-h-[540px] relative">
        <ReactFlow nodes={nodes} edges={edges} fitView>
          <Background color="#242d3c" gap={20} size={1} />
          <Controls className="bg-[#141a24] border border-[#263143] text-white fill-white" />
        </ReactFlow>

        {/* Semantic Status Legend */}
        <div className="absolute bottom-4 left-4 bg-[#121722]/95 border border-[#283446] p-3.5 rounded text-[11px] font-mono space-y-1.5 pointer-events-none shadow-md">
          <div className="font-bold text-slate-200 uppercase tracking-wider text-[10px]">
            ZTAAF Status Indicators
          </div>
          <div className="flex items-center gap-2 text-slate-200">
            <span className="w-2.5 h-2.5 rounded-full bg-emerald-500"></span>
            <span>Trust ≥ 0.70: Verified Secure Node</span>
          </div>
          <div className="flex items-center gap-2 text-slate-200">
            <span className="w-2.5 h-2.5 rounded-full bg-amber-500"></span>
            <span>0.40 - 0.70: Suspicious / Warning</span>
          </div>
          <div className="flex items-center gap-2 text-slate-200">
            <span className="w-2.5 h-2.5 rounded-full bg-rose-500"></span>
            <span>Trust &lt; 0.40: Compromised / Quarantined</span>
          </div>
          <div className="flex items-center gap-2 text-slate-200">
            <span className="w-2.5 h-2.5 rounded-full bg-rose-600 border border-white"></span>
            <span>Crypto Locked: Terminal Freeze (Rule 5)</span>
          </div>
        </div>
      </div>
    </div>
  );
}
