import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { ShieldCheck, ShieldAlert, AlertTriangle, RotateCcw, Check, Lock, RefreshCw } from 'lucide-react';

export default function AuditLog() {
  const [records, setRecords] = useState([]);
  const [selectedRecordId, setSelectedRecordId] = useState('');
  const [verificationResult, setVerificationResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [tamperSuccess, setTamperSuccess] = useState(false);
  const [error, setError] = useState(null);

  const fetchRecords = async () => {
    try {
      const res = await axios.get('http://localhost:8000/inference/');
      setRecords(res.data);
      if (res.data.length > 0 && !selectedRecordId) {
        setSelectedRecordId(res.data[0].record_id);
      }
    } catch (err) {
      console.error("Error fetching inference records", err);
    }
  };

  useEffect(() => {
    fetchRecords();
  }, []);

  const verifyRecord = async (recId = selectedRecordId) => {
    if (!recId) return;
    setLoading(true);
    setError(null);
    setTamperSuccess(false);
    try {
      const res = await axios.get(`http://localhost:8000/inference/${recId}/verify`);
      setVerificationResult(res.data);
    } catch (err) {
      setError("Record not found in cryptographic vault or server unreachable.");
      setVerificationResult(null);
    }
    setLoading(false);
  };

  const simulateTampering = async () => {
    if (!selectedRecordId) return;
    setLoading(true);
    setError(null);
    try {
      await axios.post(`http://localhost:8000/inference/${selectedRecordId}/tamper`);
      setTamperSuccess(true);
      setVerificationResult(null);
      await fetchRecords();
    } catch (err) {
      setError("Failed to tamper record.");
    }
    setLoading(false);
  };

  const resetVault = async () => {
    setLoading(true);
    setError(null);
    setTamperSuccess(false);
    setVerificationResult(null);
    try {
      await axios.post('http://localhost:8000/inference/reset');
      const res = await axios.get('http://localhost:8000/inference/');
      setRecords(res.data);
      if (res.data.length > 0) {
        setSelectedRecordId(res.data[0].record_id);
      }
    } catch (err) {
      setError("Failed to reset cryptographic vault.");
    }
    setLoading(false);
  };

  const activeRecord = records.find(r => r.record_id === selectedRecordId);

  return (
    <div className="space-y-6 max-w-5xl mx-auto">
      {/* Header & Actions */}
      <div className="flex flex-col md:flex-row md:items-end justify-between gap-4 pb-5 border-b border-[#212936]">
        <div>
          <h2 className="text-xl font-bold tracking-tight text-white">
            InferenceVault Cryptographic Audit
          </h2>
          <p className="text-slate-300 text-xs mt-1">
            ZTAAF Rules 4 & 5: Ed25519 digital signatures and offline Merkle tree anchoring for non-repudiation.
          </p>
        </div>

        <div className="flex items-center gap-2">
          <button 
            onClick={resetVault}
            disabled={loading}
            className="flex items-center gap-1.5 border border-[#2d3848] hover:border-slate-300 text-slate-200 hover:text-white bg-[#161c28] px-3 py-1.5 rounded text-xs transition-colors font-mono"
            title="Reset vault records to original untampered baseline"
          >
            <RotateCcw size={13} /> Reset Vault
          </button>
          <button 
            onClick={fetchRecords}
            disabled={loading}
            className="flex items-center gap-1.5 border border-[#2d3848] hover:border-slate-300 text-slate-200 hover:text-white bg-[#161c28] px-3 py-1.5 rounded text-xs transition-colors font-mono"
          >
            <RefreshCw size={13} /> Refresh Log
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-5">
        {/* Left Column: Signed Records List */}
        <div className="lg:col-span-5 space-y-2.5">
          <div className="text-[11px] font-mono text-slate-300 font-semibold uppercase tracking-wider flex items-center justify-between pb-1">
            <span>Signed Mission Records</span>
            <span className="text-slate-400 font-normal">{records.length} Anchors</span>
          </div>

          <div className="space-y-2.5 max-h-[520px] overflow-y-auto pr-1">
            {records.map((r) => {
              const isSelected = r.record_id === selectedRecordId;
              const isTampered = r.output?.label === 'TAMPERED_LABEL';
              return (
                <div 
                  key={r.record_id}
                  onClick={() => {
                    setSelectedRecordId(r.record_id);
                    setVerificationResult(null);
                    setTamperSuccess(false);
                  }}
                  className={`p-3.5 rounded border cursor-pointer transition-colors text-left font-mono ${
                    isSelected 
                      ? 'border-white bg-[#1a2332] shadow-sm' 
                      : 'border-[#232d3d] bg-[#141a24] hover:border-[#38475f]'
                  }`}
                >
                  <div className="flex items-center justify-between text-[11px] mb-1.5">
                    <span className="font-bold text-white flex items-center gap-1.5">
                      {r.record_id}
                      {isTampered && (
                        <span className="text-[9px] px-1.5 py-0.5 rounded bg-rose-950/80 text-rose-300 border border-rose-600 font-bold uppercase">
                          Tampered
                        </span>
                      )}
                    </span>
                    <span className="text-[10px] text-slate-400 font-mono">
                      {new Date(r.timestamp).toLocaleTimeString()}
                    </span>
                  </div>

                  <div className="text-xs text-slate-200 truncate font-sans font-medium">
                    {r.output?.target || 'Classified Vision Output'}
                  </div>

                  <div className="mt-2.5 flex items-center justify-between text-[10px] text-slate-400 font-mono">
                    <span className="text-slate-300">Conf: {((r.output?.confidence || 0.9) * 100).toFixed(0)}%</span>
                    <span className="truncate max-w-[140px]">H: {r.record_hash.substring(0, 12)}...</span>
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        {/* Right Column: Verification & Tampering Inspection */}
        <div className="lg:col-span-7 space-y-4">
          {activeRecord ? (
            <div className="border border-[#263143] bg-[#141a24] rounded-md p-5 space-y-4">
              <div className="flex flex-wrap items-center justify-between gap-3 border-b border-[#212936] pb-3">
                <div>
                  <span className="text-[10px] text-slate-400 uppercase block font-mono font-medium">Inspecting Record</span>
                  <div className="flex items-center gap-2">
                    <span className="font-mono text-base font-bold text-white">{activeRecord.record_id}</span>
                    {activeRecord.output?.label === 'TAMPERED_LABEL' && (
                      <span className="text-[9px] px-1.5 py-0.5 rounded bg-rose-950/80 text-rose-300 border border-rose-600 font-bold uppercase font-mono">
                        Tampered
                      </span>
                    )}
                  </div>
                </div>
                <div className="flex items-center gap-2">
                  <button 
                    onClick={() => verifyRecord(activeRecord.record_id)}
                    disabled={loading}
                    className="flex items-center gap-1.5 bg-white hover:bg-slate-200 text-slate-950 px-3.5 py-1.5 rounded font-semibold text-xs transition-colors disabled:opacity-50"
                  >
                    <Check size={14} /> {loading ? 'Verifying...' : 'Verify Cryptographic Seal'}
                  </button>

                  <button 
                    onClick={simulateTampering}
                    disabled={loading}
                    className="flex items-center gap-1.5 border border-amber-700/80 hover:border-amber-500 text-amber-300 bg-amber-950/40 px-3 py-1.5 rounded text-xs transition-colors font-mono font-semibold"
                    title="Silently modify classification label in database"
                  >
                    <AlertTriangle size={13} className="text-amber-400" /> Tamper Record
                  </button>

                  <button 
                    onClick={resetVault}
                    disabled={loading}
                    className="flex items-center gap-1.5 border border-[#2d3848] hover:border-slate-300 text-slate-200 hover:text-white bg-[#161c28] px-3 py-1.5 rounded text-xs transition-colors font-mono"
                    title="Restore all records to original untampered state"
                  >
                    <RotateCcw size={13} /> Reset
                  </button>
                </div>
              </div>

              {/* Forensic Details */}
              <div className="space-y-2.5 font-mono text-xs">
                <div className="text-[11px] text-slate-300 uppercase tracking-wider font-semibold">
                  Composite Cryptographic Binding:
                </div>

                <div className="border border-[#232d3d] bg-[#10141d] p-3 rounded">
                  <span className="text-[10px] text-slate-400 block uppercase font-medium">Output Classification Payload</span>
                  <span className="text-slate-100 font-semibold block mt-0.5 break-all">
                    {JSON.stringify(activeRecord.output)}
                  </span>
                </div>

                <div className="border border-[#232d3d] bg-[#10141d] p-2.5 rounded truncate">
                  <span className="text-[10px] text-slate-400 block uppercase font-medium">Input Image SHA-256</span>
                  <span className="text-slate-200">{activeRecord.input_hash}</span>
                </div>

                <div className="border border-[#232d3d] bg-[#10141d] p-2.5 rounded truncate">
                  <span className="text-[10px] text-slate-400 block uppercase font-medium">Model Weights Digest</span>
                  <span className="text-slate-200">{activeRecord.model_digest}</span>
                </div>

                <div className="border border-[#232d3d] bg-[#10141d] p-2.5 rounded truncate">
                  <span className="text-[10px] text-slate-400 block uppercase font-medium">Ed25519 Asymmetric Signature</span>
                  <span className="text-slate-300">{activeRecord.signature}</span>
                </div>
              </div>

              {/* Tamper Alert Notice */}
              {tamperSuccess && (
                <div className="border border-amber-500 bg-amber-950/50 p-4 rounded text-xs font-mono space-y-1.5">
                  <div className="text-amber-300 font-bold flex items-center gap-1.5">
                    <AlertTriangle size={15} className="text-amber-400" />
                    Adversary Simulation Injected
                  </div>
                  <p className="text-amber-100 font-sans text-xs leading-relaxed">
                    The database was altered to mutate the classification label without cryptographic re-signing. Click <strong className="text-white underline">Verify Cryptographic Seal</strong> above to inspect the mathematical failure.
                  </p>
                </div>
              )}

              {/* Verification Results */}
              {verificationResult && verificationResult.status === 'success' && (
                <div className="border border-emerald-500 bg-emerald-950/50 p-4 rounded text-xs space-y-1.5">
                  <div className="flex items-center gap-2 text-emerald-300 font-bold tracking-wide font-mono">
                    <ShieldCheck size={18} className="text-emerald-400" /> Cryptographic Seal Verified Valid
                  </div>
                  <p className="text-slate-100 font-sans text-xs leading-relaxed">
                    SHA-256 composite hash, Ed25519 signature, and offline Merkle tree leaf are genuine and untampered. Complete non-repudiation verified.
                  </p>
                  <div className="text-[11px] text-emerald-300 font-mono pt-1">
                    ✓ Nonce: {activeRecord.sequence_nonce} · Verified at: {new Date().toLocaleTimeString()}
                  </div>
                </div>
              )}

              {verificationResult && verificationResult.status === 'failed' && (
                <div className="border-2 border-rose-500 bg-rose-950/60 p-4 rounded text-xs space-y-2">
                  <div className="flex items-center gap-2 text-rose-300 font-bold tracking-wide font-mono">
                    <ShieldAlert size={18} className="text-rose-400" /> Cryptographic Integrity Failure Detected
                  </div>
                  <p className="text-rose-200 font-mono text-xs font-bold">
                    {verificationResult.reason}
                  </p>
                  <p className="text-slate-100 font-sans text-xs leading-relaxed">
                    The record bytes were modified after creation. The recomputed composite hash failed to match the author's Ed25519 signature.
                  </p>
                </div>
              )}

              {error && (
                <div className="border border-slate-700 bg-slate-900 p-3 rounded text-xs text-slate-200 font-mono flex items-center gap-2">
                  <ShieldAlert size={14} className="text-rose-400" /> {error}
                </div>
              )}
            </div>
          ) : (
            <div className="border border-dashed border-[#2d3848] rounded-md p-12 text-center text-slate-400 text-xs">
              Select a record from the audit log to inspect its cryptographic seal.
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
