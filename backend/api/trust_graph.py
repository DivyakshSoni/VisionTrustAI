from fastapi import APIRouter, HTTPException
from typing import List
from backend.core.schemas.schemas import TrustNodeSchema

router = APIRouter(prefix="/graph", tags=["AssuranceHub"])

# Mock database for demonstration
NODES_DB = {}

@router.get("/nodes", response_model=List[TrustNodeSchema])
def list_nodes():
    """Returns all trust nodes for D3/Recharts rendering."""
    # Convert internal TrustNode to Schema
    output = []
    for node in NODES_DB.values():
        output.append(TrustNodeSchema(
            node_id=node.id,
            node_type=node.type,
            trust_score=node.trust,
            crypto_locked=node.crypto_locked,
            propagated_to=[n.id for n in node.downstream_edges]
        ))
    return output

@router.get("/nodes/{node_id}")
def get_node(node_id: str):
    """Gets a specific node and its evidence history."""
    if node_id not in NODES_DB:
        raise HTTPException(status_code=404, detail="Node not found")
    return NODES_DB[node_id]

@router.get("/propagation-history")
def get_propagation_history():
    """
    Returns edge connections to show how distrust propagated through the system.
    Useful for the TrustGraphView.jsx component.
    """
    edges = []
    for node in NODES_DB.values():
        for downstream in node.downstream_edges:
            edges.append({"source": node.id, "target": downstream.id})
    return {"edges": edges}
