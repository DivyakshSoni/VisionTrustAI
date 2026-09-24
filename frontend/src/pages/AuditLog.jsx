import React, { useState } from 'react';
import axios from 'axios';
import { Search, ShieldCheck, ShieldAlert } from 'lucide-react';

export default function AuditLog() {
  const [recordId, setRecordId] = useState('');
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const verifyRecord = async () => {
    try {
      setError(null);
      const res = await axios.get(`http://localhost:8000/inference/${recordId}/verify`);
      setResult(res.data);
    } catch (err) {
      setError("Record not found or verification failed.");
      setResult(null);
    }
  };

  return (
    <div className="space-y-6">
      <h2 className="text-3xl font-bold bg-gradient-to-r from-primary to-accent bg-clip-text text-transparent">
        InferenceVault Audit
      </h2>
      <p className="text-slate-400">Verify the cryptographic integrity of a specific inference record against the Merkle tree.</p>
      
      <div className="flex gap-4 max-w-xl">
        <input 
          type="text" 
          value={recordId}
          onChange={(e) => setRecordId(e.target.value)}
          placeholder="Enter Record ID (e.g., INF-A1B2C3D4)"
          className="flex-1 bg-dark border border-slate-700 rounded-lg px-4 py-2 text-slate-200 focus:outline-none focus:border-primary"
        />
        <button 
          onClick={verifyRecord}
          className="bg-primary hover:bg-blue-600 text-white px-6 py-2 rounded-lg flex items-center gap-2 transition"
        >
          <Search size={18} /> Verify
        </button>
      </div>

      {error && (
        <div className="p-4 bg-red-900/20 border border-red-500/50 rounded-lg text-red-400 flex items-center gap-3">
          <ShieldAlert size={24} /> {error}
        </div>
      )}

      {result && result.status === 'success' && (
        <div className="p-6 bg-green-900/20 border border-green-500/50 rounded-lg text-green-400 flex flex-col gap-3">
          <div className="flex items-center gap-3 text-xl font-bold">
            <ShieldCheck size={28} /> Verification Passed
          </div>
          <p className="text-sm">Record <strong>{result.record_id}</strong> is cryptographically sound. Hash, Ed25519 signature, and Merkle Path are valid.</p>
        </div>
      )}

      {result && result.status === 'failed' && (
        <div className="p-6 bg-red-900/20 border border-red-500/50 rounded-lg text-red-400 flex flex-col gap-3">
          <div className="flex items-center gap-3 text-xl font-bold">
            <ShieldAlert size={28} /> Verification Failed
          </div>
          <p className="text-sm font-bold">CRITICAL WARNING: {result.reason}</p>
        </div>
      )}
    </div>
  );
}
