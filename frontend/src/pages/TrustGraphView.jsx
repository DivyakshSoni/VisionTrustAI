import React, { useEffect, useState } from 'react';
import axios from 'axios';
import ReactFlow, { Background, Controls } from 'reactflow';
import 'reactflow/dist/style.css';

export default function TrustGraphView() {
  const [nodes, setNodes] = useState([]);
  const [edges, setEdges] = useState([]);

  useEffect(() => {
    const fetchGraph = async () => {
      try {
        const nodeRes = await axios.get('http://localhost:8000/graph/nodes');
        const edgeRes = await axios.get('http://localhost:8000/graph/propagation-history');
        
        // Format for ReactFlow
        const formattedNodes = nodeRes.data.map((n, i) => ({
          id: n.node_id,
          position: { x: 250 * i, y: i % 2 === 0 ? 100 : 250 },
          data: { 
            label: (
              <div className="text-center p-2">
                <div className="font-bold text-slate-800">{n.node_type.toUpperCase()}</div>
                <div className={`font-mono mt-1 ${n.trust_score < 0.5 ? 'text-danger' : 'text-accent'}`}>
                  Trust: {n.trust_score.toFixed(2)}
                </div>
                {n.crypto_locked && <div className="text-xs text-danger font-bold mt-1">CRYPTO LOCKED</div>}
              </div>
            ) 
          },
          style: {
            background: n.trust_score < 0.5 ? '#fecaca' : '#bbf7d0',
            border: '2px solid #334155',
            borderRadius: '8px',
            width: 180
          }
        }));

        const formattedEdges = edgeRes.data.edges.map((e, i) => ({
          id: `e${i}`,
          source: e.source,
          target: e.target,
          animated: true,
          style: { stroke: '#ef4444', strokeWidth: 2 }
        }));

        setNodes(formattedNodes);
        setEdges(formattedEdges);
      } catch (err) {
        console.error(err);
      }
    };
    fetchGraph();
  }, []);

  return (
    <div className="h-full flex flex-col space-y-4">
      <div>
        <h2 className="text-3xl font-bold bg-gradient-to-r from-primary to-accent bg-clip-text text-transparent">
          Trust Propagation Graph
        </h2>
        <p className="text-slate-400 mt-2">Visualizing ZTAAF Principle 3: Distrust propagates to dependent nodes.</p>
      </div>
      
      <div className="flex-1 bg-slate-900 border border-slate-800 rounded-xl overflow-hidden min-h-[600px]">
        <ReactFlow nodes={nodes} edges={edges} fitView>
          <Background color="#334155" gap={16} />
          <Controls />
        </ReactFlow>
      </div>
    </div>
  );
}
