# ZTAAF Architecture & Principles

## The Core Principles
The VisionTrust AI platform enforces the 5 core principles of the Zero-Trust AI Assurance Framework:
1. **Never Trust, Always Verify:** AI models and datasets start at a low prior trust score (0.2), requiring constant affirmative evidence to be utilized.
2. **Architectural Independence:** Evidence is weighted heavily if it comes from different modalities (e.g., classical LBP textures vs CLIP embeddings) via the `independence_factor`.
3. **Distrust Propagates Faster than Trust:** A severe security finding on a dataset immediately drops its trust score. This distrust propagates recursively to any models trained on it.
4. **Assume the Verifier is Breached:** All assurance modules (detectors) must pass a frozen `CanaryGate` test before their evidence is accepted by TrustFlow.
5. **Cryptographic Floor:** If a cryptographic signature fails in `InferenceVault`, trust is permanently locked to `0.0`.

## Module Layout
- `/backend/modules/dataguard/`: Dataset integrity checks (duplicates, label consistency, poisoning).
- `/backend/modules/modelshield/`: Model integrity checks (fingerprinting, neural cleanse).
- `/backend/modules/inferencevault/`: Immutable cryptographic binding of inference records.
- `/backend/modules/driftlens/`: Real-time operational drift detection via MMD and PSI.
- `/backend/modules/redforge/`: Adversarial attack injection for automated red-teaming.
- `/backend/core/sentinelcore/`: The Trust Graph and TrustFlow algorithm orchestration.
