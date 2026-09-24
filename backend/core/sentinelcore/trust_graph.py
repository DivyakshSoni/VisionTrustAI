from typing import List

# Reference multipliers for ZTAAF Principles
DISCONFIRM_MULTIPLIER = 4.0
MAX_TRUST = 1.0
MIN_TRUST = 0.0

class Evidence:
    def __init__(self, detector_id: str, direction: str, weight: float, architecture_family: str, canary_passed: bool):
        self.detector_id = detector_id
        self.direction = direction  # 'confirm', 'disconfirm', 'crypto_failure', 'crypto_success'
        self.weight = weight
        self.architecture_family = architecture_family  # e.g., 'cnn_embedding', 'classical_stats'
        self.canary_passed = canary_passed

class TrustNode:
    def __init__(self, node_id: str, node_type: str):
        self.id = node_id
        self.type = node_type
        self.trust = 0.2  # Principle 1: low prior
        self.crypto_locked = False
        self.downstream_edges: List['TrustNode'] = []
        self.evidence_history: List[Evidence] = []

def independence_factor(evidence: Evidence, existing_evidence: List[Evidence]) -> float:
    """
    Discounts confirming evidence if the architecture family has already contributed.
    Principle 2: Corroboration requires architecturally independent sources.
    """
    matching_arch_count = sum(
        1 for e in existing_evidence 
        if e.direction == 'confirm' and e.architecture_family == evidence.architecture_family
    )
    # Discount factor: 1.0 for first, 0.5 for second, 0.25 for third, etc.
    return 1.0 / (2 ** matching_arch_count)

def update_trust(node: TrustNode, new_evidence_list: List[Evidence]):
    """
    Core TrustFlow update algorithm matching the ZTAAF update rule.
    """
    if node.crypto_locked:
        return  # Principle 5: Cryptographic failures are terminal

    significant_change_threshold = 0.15
    old_trust = node.trust

    for e in new_evidence_list:
        if e.direction == 'crypto_failure':
            node.trust = MIN_TRUST
            node.crypto_locked = True
            node.evidence_history.append(e)
            # Implements terminal lock and triggers propagation
            from .propagation import propagate_distrust
            propagate_distrust(node, reason="Cryptographic verification failed.")
            return  
            
        if e.direction == 'crypto_success':
            # Crypto clears suspicion only if there is no active ML disconfirmation
            has_disconfirm = any(ev.direction == 'disconfirm' for ev in node.evidence_history)
            if not has_disconfirm:
                node.trust = min(node.trust + 0.5, MAX_TRUST)
            node.evidence_history.append(e)
            continue

        if not e.canary_passed:
            continue  # Principle 4: Unverified detectors contribute nothing

        if e.direction == 'confirm':
            factor = independence_factor(e, node.evidence_history)
            node.trust += (e.weight * factor)
        elif e.direction == 'disconfirm':
            # Principle 3: Disconfirming evidence is weighted asymmetrically
            node.trust -= (e.weight * DISCONFIRM_MULTIPLIER)
            
        node.evidence_history.append(e)

    node.trust = max(MIN_TRUST, min(node.trust, MAX_TRUST))

    # Propagate distrust if there was a significant drop
    if (old_trust - node.trust) > significant_change_threshold:
        from .propagation import propagate_distrust
        propagate_distrust(node, reason=f"Significant trust drop from {old_trust:.2f} to {node.trust:.2f}")
