from fastapi import APIRouter, HTTPException
from typing import List
from backend.core.schemas.schemas import FindingSchema
from backend.llm.explain import generate_finding_summary

router = APIRouter(prefix="/findings", tags=["AssuranceHub"])

# Mock database for demonstration
FINDINGS_DB = []

@router.get("/", response_model=List[FindingSchema])
def list_findings():
    """Returns all findings for the AssuranceHub dashboard."""
    return FINDINGS_DB

@router.get("/{finding_id}")
def get_finding(finding_id: str):
    """Gets a specific finding."""
    finding = next((f for f in FINDINGS_DB if f.finding_id == finding_id), None)
    if not finding:
        raise HTTPException(status_code=404, detail="Finding not found")
    return finding

@router.get("/{finding_id}/explain")
def explain_finding(finding_id: str):
    """Uses the local LLM to generate a summary for a specific finding."""
    finding = next((f for f in FINDINGS_DB if f.finding_id == finding_id), None)
    if not finding:
        raise HTTPException(status_code=404, detail="Finding not found")
        
    explanation = generate_finding_summary(finding.model_dump())
    return {"finding_id": finding_id, "explanation": explanation}
