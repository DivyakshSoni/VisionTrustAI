from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Dict, Any

from backend.modules.inferencevault.record_binding import create_inference_record
from backend.modules.inferencevault.verification import verify_inference_record
from backend.core.crypto.signing import generate_keypair
from backend.core.schemas.schemas import InferenceRecordSchema
from backend.core.crypto.merkle import MerkleTree

router = APIRouter(prefix="/inference", tags=["InferenceVault"])

# For demonstration, we keep an in-memory store and keypair.
# In a real app, these would come from the database/secret manager.
MOCK_PRIVATE_KEY, MOCK_PUBLIC_KEY = generate_keypair()
INFERENCE_STORE: Dict[str, InferenceRecordSchema] = {}
MERKLE_LEAVES = []

class InferenceRequest(BaseModel):
    input_hash: str
    model_digest: str
    preprocessing_config_hash: str
    inference_config_hash: str
    output: Dict[str, Any]

@router.post("/", response_model=InferenceRecordSchema)
def create_inference(req: InferenceRequest):
    record = create_inference_record(
        input_hash=req.input_hash,
        model_digest=req.model_digest,
        preprocessing_config_hash=req.preprocessing_config_hash,
        inference_config_hash=req.inference_config_hash,
        output=req.output,
        private_key=MOCK_PRIVATE_KEY
    )
    
    INFERENCE_STORE[record.record_id] = record
    MERKLE_LEAVES.append(record.record_hash)
    
    return record

@router.get("/{record_id}/verify")
def verify_inference(record_id: str):
    if record_id not in INFERENCE_STORE:
        raise HTTPException(status_code=404, detail="Record not found")
        
    record = INFERENCE_STORE[record_id]
    
    # Rebuild tree for demo verification
    tree = MerkleTree(MERKLE_LEAVES)
    
    is_valid = verify_inference_record(record, MOCK_PUBLIC_KEY, tree)
    
    if not is_valid:
        return {"status": "failed", "reason": "Cryptographic mismatch detected (hash, signature, or Merkle log)."}
        
    return {"status": "success", "record_id": record.record_id}
    
@router.post("/{record_id}/tamper")
def tamper_inference(record_id: str):
    """
    Demonstration endpoint to silently alter a record byte.
    """
    if record_id not in INFERENCE_STORE:
        raise HTTPException(status_code=404, detail="Record not found")
        
    record = INFERENCE_STORE[record_id]
    # Simulate an attacker changing the output label without changing the signature
    record.output["label"] = "TAMPERED_LABEL"
    
    return {"status": "tampered", "message": f"Record {record_id} silently altered in database"}
