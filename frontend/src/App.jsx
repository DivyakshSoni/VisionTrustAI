import React from 'react';
import { BrowserRouter, Routes, Route, Link } from 'react-router-dom';
import Dashboard from './pages/Dashboard';
import TrustGraphView from './pages/TrustGraphView';
import AuditLog from './pages/AuditLog';
import { Shield, GitCommit, FileSearch, Lock } from 'lucide-react';

function App() {
  return (
    <BrowserRouter>
      <div className="min-h-screen bg-darker text-slate-200 flex">
        {/* Sidebar */}
        <aside className="w-64 bg-dark border-r border-slate-800 p-4">
          <div className="flex items-center gap-3 mb-8 text-primary">
            <Shield size={32} />
            <h1 className="text-xl font-bold">VisionTrust AI</h1>
          </div>
          <nav className="flex flex-col gap-2">
            <Link to="/" className="flex items-center gap-2 p-3 rounded-lg hover:bg-slate-800 transition">
              <FileSearch size={20} /> Findings
            </Link>
            <Link to="/graph" className="flex items-center gap-2 p-3 rounded-lg hover:bg-slate-800 transition">
              <GitCommit size={20} /> Trust Graph
            </Link>
            <Link to="/audit" className="flex items-center gap-2 p-3 rounded-lg hover:bg-slate-800 transition">
              <Lock size={20} /> Inference Audit
            </Link>
          </nav>
        </aside>

        {/* Main Content */}
        <main className="flex-1 p-8">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/graph" element={<TrustGraphView />} />
            <Route path="/audit" element={<AuditLog />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  );
}

export default App;
