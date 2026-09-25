import uuid
from typing import Dict, Any, List

from backend.core.schemas.schemas import TrustNodeSchema, EvidenceEvent, FindingSchema, AssetRef
from backend.core.sentinelcore.trust_graph import TrustNode, Evidence, update_trust
from backend.core.sentinelcore.canary import gate as canary_gate
from backend.modules.dataguard.duplicates import find_phash_duplicates
from backend.api.trust_graph import NODES_DB
from backend.api.findings import FINDINGS_DB

def create_node(node_type: str) -> TrustNode:
    node_id = f"{node_type.upper()}-{uuid.uuid4().hex[:6]}"
    node = TrustNode(node_id=node_id, node_type=node_type)
    # Register in the global DB for the API
    NODES_DB[node_id] = node
    return node

def link_nodes(upstream: TrustNode, downstream: TrustNode):
    upstream.downstream_edges.append(downstream)
    
def run_dataset_assurance(dataset_paths: List[str], batch_node: TrustNode, force_poison: bool = False):
    """
    Example workflow integrating DataGuard and TrustFlow.
    """
    # 1. Canary check for the detector 
    detector_id = "dataguard_phash"
    canary_passed = canary_gate.has_passed(detector_id) 
    if detector_id not in canary_gate.canary_results:
        canary_passed = canary_gate.run_canary_test(detector_id, lambda x: True, None, True)
    
    # 2. Run detector
    duplicates = find_phash_duplicates(dataset_paths, threshold=5)
    
    if force_poison:
        duplicates = [("img1.jpg", "img2.jpg"), ("img3.jpg", "img4.jpg")] # Mock finding
        
    # 3. Generate Findings and Evidence
    evidence_events = []
    
    if duplicates:
        # Create a finding
        finding = FindingSchema(
            finding_id=f"FND-{uuid.uuid4().hex[:6]}",
            module="DataGuard",
            affected_asset=AssetRef(type="dataset_batch", id=batch_node.id),
            reason=f"Found {len(duplicates)} near-duplicate pairs indicating a duplicate flood attack.",
            evidence={"duplicate_pairs": duplicates},
            trust_score_before=batch_node.trust,
            trust_score_after=0.0, # Will be updated
            confidence=0.95,
            severity="high",
            recommended_action="quarantine",
            limitations="pHash is susceptible to heavy cropping."
        )
        
        # Create TrustFlow evidence
        ev = Evidence(
            detector_id=detector_id,
            direction="disconfirm",
            weight=0.3,
            architecture_family="classical_hashing",
            canary_passed=canary_passed
        )
        evidence_events.append(ev)
        
    else:
        finding = None
        ev = Evidence(
            detector_id=detector_id,
            direction="confirm",
            weight=0.1,
            architecture_family="classical_hashing",
            canary_passed=canary_passed
        )
        evidence_events.append(ev)
        
    # 4. Update Trust Graph
    old_trust = batch_node.trust
    update_trust(batch_node, evidence_events)
    
    if finding:
        finding.trust_score_after = batch_node.trust
        FINDINGS_DB.append(finding)
        
    return batch_node.trust

    return batch_node.trust

def reset_pipeline():
    """
    Resets the trust graph and findings database to a clean baseline state.
    """
    NODES_DB.clear()
    FINDINGS_DB.clear()
    
    contributor = create_node("contributor")
    contributor.trust = 0.85
    
    dataset_batch = create_node("dataset_batch")
    dataset_batch.trust = 0.80
    
    model = create_node("model")
    model.trust = 0.75
    
    inference_service = create_node("inference_service")
    inference_service.trust = 0.80
    
    link_nodes(contributor, dataset_batch)
    link_nodes(dataset_batch, model)
    link_nodes(model, inference_service)
    
    return {"status": "Pipeline reset to clean operational baseline.", "nodes_count": len(NODES_DB)}

def run_demo_pipeline(attack_type: str = "duplicate_flood"):
    """
    Runs the end-to-end demo pipeline to populate the databases.
    Supports: 'duplicate_flood' (DataGuard), 'backdoor' (ModelShield), 'drift' (DriftLens).
    """
    if not NODES_DB:
        reset_pipeline()
        
    nodes = list(NODES_DB.values())
    dataset_batch = next((n for n in nodes if n.type == "dataset_batch"), None)
    model = next((n for n in nodes if n.type == "model"), None)
    inference_node = next((n for n in nodes if n.type == "inference_service"), None)
    
    if not dataset_batch or not model:
        reset_pipeline()
        nodes = list(NODES_DB.values())
        dataset_batch = next((n for n in nodes if n.type == "dataset_batch"), None)
        model = next((n for n in nodes if n.type == "model"), None)
        inference_node = next((n for n in nodes if n.type == "inference_service"), None)

    if attack_type == "backdoor":
        # ModelShield detects backdoor trigger pattern
        detector_id = "modelshield_cleanse"
        canary_passed = canary_gate.has_passed(detector_id)
        if detector_id not in canary_gate.canary_results:
            canary_passed = canary_gate.run_canary_test(detector_id, lambda x: True, None, True)
            
        old_trust = model.trust
        ev = Evidence(
            detector_id=detector_id,
            direction="crypto_failure",
            weight=1.0,
            architecture_family="adversarial_optimization",
            canary_passed=canary_passed
        )
        update_trust(model, [ev])
        
        finding = FindingSchema(
            finding_id=f"FND-{uuid.uuid4().hex[:6]}",
            module="ModelShield",
            affected_asset=AssetRef(type="model", id=model.id),
            reason="Abnormally small L1 perturbation mask detected by Neural Cleanse Lite. Backdoor trigger confirmed.",
            evidence={"target_class": "civilian_vehicle", "trigger_size_px": 12, "anomaly_index": 3.42},
            trust_score_before=old_trust,
            trust_score_after=model.trust,
            confidence=0.98,
            severity="critical",
            recommended_action="immediate_quarantine",
            limitations="Assumes single-target backdoor injection."
        )
        FINDINGS_DB.append(finding)
        return {"status": "ModelShield Backdoor Attack simulated. Model crypto-locked.", "attack": attack_type}
        
    elif attack_type == "drift":
        # DriftLens detects environmental distribution shift
        detector_id = "driftlens_psi"
        canary_passed = canary_gate.has_passed(detector_id)
        if detector_id not in canary_gate.canary_results:
            canary_passed = canary_gate.run_canary_test(detector_id, lambda x: True, None, True)
            
        target_node = inference_node or model
        old_trust = target_node.trust
        ev = Evidence(
            detector_id=detector_id,
            direction="disconfirm",
            weight=0.15,
            architecture_family="distributional_statistics",
            canary_passed=canary_passed
        )
        update_trust(target_node, [ev])
        
        finding = FindingSchema(
            finding_id=f"FND-{uuid.uuid4().hex[:6]}",
            module="DriftLens",
            affected_asset=AssetRef(type="inference_service", id=target_node.id),
            reason="Population Stability Index (PSI = 0.28 > 0.20) indicates significant environmental drift in target camera angle and sandstorm fog.",
            evidence={"psi_score": 0.28, "mmd_distance": 0.142, "baseline_window": "2026-Q1"},
            trust_score_before=old_trust,
            trust_score_after=target_node.trust,
            confidence=0.91,
            severity="medium",
            recommended_action="recalibrate_sensors",
            limitations="Drift metrics require minimum 200 frame sample size."
        )
        FINDINGS_DB.append(finding)
        return {"status": "DriftLens Environmental Shift detected.", "attack": attack_type}

    else:
        # Default: DataGuard Duplicate Flood attack
        run_dataset_assurance(["dummy_img1.jpg", "dummy_img2.jpg"], dataset_batch, force_poison=True)
        return {"status": "DataGuard Poisoning attack executed. Distrust propagated.", "attack": "duplicate_flood"}
