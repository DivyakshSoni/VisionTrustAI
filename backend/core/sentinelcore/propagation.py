from typing import List

DISTRUST_PROPAGATION_FACTOR = 0.5

def propagate_distrust(node, reason: str):
    """
    Propagates distrust down the graph edges.
    Principle 3: Distrust propagates to dependent nodes automatically.
    """
    for dependent in node.downstream_edges:
        if not dependent.crypto_locked:
            dependent.trust = dependent.trust * DISTRUST_PROPAGATION_FACTOR
            print(f"[TrustFlow] FLAG: Node {dependent.id} trust reduced to {dependent.trust:.2f} due to: {reason}")
            # Recursively propagate down the chain
            propagate_distrust(dependent, reason=f"Upstream node {node.id} lost trust")
