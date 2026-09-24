# VisionTrust AI: Zero-Trust AI Assurance Framework (ZTAAF)
**SIH26228 | Ministry of Defence (MoD) | Indian Army (DGIS)**
**Theme:** Blockchain & Cybersecurity

VisionTrust AI is an air-gapped, zero-trust cryptographic assurance platform designed to defend military Computer Vision models against adversarial attacks, data poisoning, and operational drift.

## 🚀 Features

- **DataGuard:** Detects data poisoning, duplicate-flooding, and OOD (Out-of-Distribution) samples using architecturally independent classical and deep features.
- **ModelShield:** Ensures model integrity via cryptographic digests, behavioral fingerprinting (black-box), and Neural-Cleanse-Lite (white-box backdoor detection).
- **InferenceVault:** Cryptographically binds model inferences to inputs and configurations, hashing them into a Merkle Tree for an immutable audit trail.
- **SentinelCore (TrustFlow):** A dynamic Trust Graph that penalizes compromised nodes. Distrust propagates automatically downstream to dependent models (ZTAAF Principle 3).
- **RedForge:** A built-in adversarial testing suite to inject attacks (label flipping, patch backdoors) to prove the framework's efficacy.

## 🛠️ Tech Stack
- **Backend**: Python, FastAPI, PyTorch, Cryptography (Ed25519, SHA-256), OpenCV, Scikit-learn
- **Frontend**: React, Vite, TailwindCSS, ReactFlow (for interactive Trust Graph visualization)

## 🏁 Quickstart (Demo Mode)
To run the full end-to-end prototype and demonstrate TrustFlow propagation:

1. **Start the Backend API:**
   ```bash
   uvicorn backend.main:app --reload
   ```
2. **Start the AssuranceHub Dashboard (in a new terminal):**
   ```bash
   cd frontend
   npm run dev
   ```
3. Open `http://localhost:5173` in your browser.
4. Click **"Run ZTAAF Demo"** in the top right to simulate a data-poisoning attack and watch the Trust Graph autonomously quarantine the compromised assets.
