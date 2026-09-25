import React from 'react';
import { BrowserRouter, Routes, Route, Link, useLocation } from 'react-router-dom';
import Dashboard from './pages/Dashboard';
import TrustGraphView from './pages/TrustGraphView';
import AuditLog from './pages/AuditLog';
import { Shield, GitCommit, FileSearch, Lock } from 'lucide-react';

function Navigation() {
  const location = useLocation();

  const navItems = [
    { path: '/', label: 'Assurance Findings', icon: <FileSearch size={17} /> },
    { path: '/graph', label: 'Trust Graph', icon: <GitCommit size={17} /> },
    { path: '/audit', label: 'InferenceVault Audit', icon: <Lock size={17} /> },
  ];

  return (
    <nav className="flex flex-col gap-1.5">
      {navItems.map((item) => {
        const isActive = location.pathname === item.path;
        return (
          <Link
            key={item.path}
            to={item.path}
            className={`flex items-center gap-3 px-3.5 py-2.5 rounded-md text-xs tracking-wide transition-colors ${
              isActive
                ? 'bg-white text-black font-semibold shadow-sm'
                : 'text-slate-300 hover:text-white hover:bg-slate-800/70 font-normal'
            }`}
          >
            {item.icon} {item.label}
          </Link>
        );
      })}
    </nav>
  );
}

function App() {
  return (
    <BrowserRouter>
      <div className="min-h-screen bg-[#0b0f15] text-[#f8fafc] flex antialiased">
        {/* Sidebar */}
        <aside className="w-64 bg-[#111620] border-r border-[#212936] p-5 flex flex-col justify-between select-none">
          <div>
            <div className="flex items-center gap-3 mb-6 pb-4 border-b border-[#212936]">
              <div className="w-8 h-8 rounded border border-slate-600 bg-slate-800 flex items-center justify-center text-white font-mono font-bold text-sm">
                ZT
              </div>
              <div>
                <h1 className="text-sm font-semibold tracking-tight text-white">VisionTrust AI</h1>
                <span className="text-[10px] text-slate-400 block tracking-wider uppercase font-mono">
                  ZTAAF v0.1.0
                </span>
              </div>
            </div>

            <div className="mb-6 px-3 py-2 rounded border border-[#283242] bg-[#161c28] text-[11px] font-mono text-slate-200 flex items-center justify-between">
              <span className="flex items-center gap-2">
                <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
                AIR-GAPPED
              </span>
              <span className="text-[10px] text-emerald-400 font-semibold tracking-wide">SEC-READY</span>
            </div>

            <Navigation />
          </div>

          <div className="border-t border-[#212936] pt-4 text-[11px] font-mono space-y-1">
            <div className="text-slate-200 font-semibold tracking-tight">SIH26228 Specification</div>
            <div className="text-slate-400">Indian Army · DGIS</div>
            <div className="text-[10px] text-slate-500">Multi-Contributor Vision Pipeline</div>
          </div>
        </aside>

        {/* Main Content */}
        <main className="flex-1 p-8 overflow-y-auto">
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
