from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime

class EvidenceEvent(BaseModel):
    detector: str
    direction: str # 'confirm' or 'disconfirm'
    weight: float
    canary_passed: bool

class TrustNodeSchema(BaseModel):
    node_id: str
    node_type: str
    trust_score: float = 0.2
    crypto_locked: bool = False
    last_updated: datetime = Field(default_factory=datetime.utcnow)
    contributing_evidence: List[EvidenceEvent] = []
    propagated_from: List[str] = []
    propagated_to: List[str] = []

class AssetRef(BaseModel):
    type: str
    id: str
    contributor: Optional[str] = None

class FindingSchema(BaseModel):
    finding_id: str
    module: str
    affected_asset: AssetRef
    reason: str
    evidence: Dict[str, Any]
    trust_score_before: float
    trust_score_after: float
    confidence: float
    severity: str
    recommended_action: str
    limitations: str

class InferenceRecordSchema(BaseModel):
    record_id: str
    input_hash: str
    model_digest: str
    preprocessing_config_hash: str
    inference_config_hash: str
    output: Dict[str, Any]
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    sequence_nonce: str
    record_hash: str
    signature: str
    crypto_verified: bool
