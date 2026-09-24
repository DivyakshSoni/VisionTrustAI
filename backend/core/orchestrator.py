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

def run_demo_pipeline():
    """
    Runs the end-to-end demo pipeline to populate the databases.
    """
    # Create the graph
    contributor = create_node("contributor")
    dataset_batch = create_node("dataset_batch")
    model = create_node("model")
    
    link_nodes(contributor, dataset_batch)
    link_nodes(dataset_batch, model)
    
    # Run assurance (mocking an attack to show distrust propagation)
    run_dataset_assurance(["dummy_img1.jpg", "dummy_img2.jpg"], dataset_batch, force_poison=True)
    
    return {"status": "Pipeline executed. Check /graph/nodes and /findings APIs."}
