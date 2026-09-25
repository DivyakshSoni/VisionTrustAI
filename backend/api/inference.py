from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Dict, Any, List

from backend.modules.inferencevault.record_binding import create_inference_record
from backend.modules.inferencevault.verification import verify_inference_record
from backend.core.crypto.signing import generate_keypair
from backend.core.schemas.schemas import InferenceRecordSchema
from backend.core.crypto.merkle import MerkleTree

router = APIRouter(prefix="/inference", tags=["InferenceVault"])

# For demonstration, we keep an in-memory store and keypair.
MOCK_PRIVATE_KEY, MOCK_PUBLIC_KEY = generate_keypair()
INFERENCE_STORE: Dict[str, InferenceRecordSchema] = {}
MERKLE_LEAVES = []

def seed_demo_records():
    if INFERENCE_STORE:
        return
    demos = [
        {
            "input_hash": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
            "model_digest": "4a8f3b2e1c9d8a7b6c5d4e3f2a1b0c9d8e7f6a5b4c3d2e1f0a9b8c7d6e5f4a3b",
            "preprocessing_config_hash": "d2f4a56b7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f",
            "inference_config_hash": "112233445566778899aabbccddeeff00112233445566778899aabbccddeeff00",
            "output": {"target": "Armored Vehicle (T-90)", "confidence": 0.94, "sector": "Northern Sector Alpha", "threat_level": "High"}
        },
        {
            "input_hash": "a1b2c3d4e5f60718293a4b5c6d7e8f90123456789abcdef0123456789abcdef0",
            "model_digest": "4a8f3b2e1c9d8a7b6c5d4e3f2a1b0c9d8e7f6a5b4c3d2e1f0a9b8c7d6e5f4a3b",
            "preprocessing_config_hash": "d2f4a56b7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f",
            "inference_config_hash": "112233445566778899aabbccddeeff00112233445566778899aabbccddeeff00",
            "output": {"target": "Runway Intrusion Detected", "confidence": 0.89, "coordinates": "34.0837 N, 74.7973 E", "threat_level": "Medium"}
        },
        {
            "input_hash": "9f8e7d6c5b4a3210fedcba9876543210abcdef0123456789abcdef0123456789",
            "model_digest": "4a8f3b2e1c9d8a7b6c5d4e3f2a1b0c9d8e7f6a5b4c3d2e1f0a9b8c7d6e5f4a3b",
            "preprocessing_config_hash": "d2f4a56b7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f",
            "inference_config_hash": "112233445566778899aabbccddeeff00112233445566778899aabbccddeeff00",
            "output": {"target": "Friendly Logistics Supply Truck", "confidence": 0.97, "gate": "Checkpoint Bravo", "threat_level": "None"}
        }
    ]
    for d in demos:
        record = create_inference_record(
            input_hash=d["input_hash"],
            model_digest=d["model_digest"],
            preprocessing_config_hash=d["preprocessing_config_hash"],
            inference_config_hash=d["inference_config_hash"],
            output=d["output"],
            private_key=MOCK_PRIVATE_KEY
        )
        INFERENCE_STORE[record.record_id] = record
        MERKLE_LEAVES.append(record.record_hash)

seed_demo_records()

class InferenceRequest(BaseModel):
    input_hash: str
    model_digest: str
    preprocessing_config_hash: str
    inference_config_hash: str
    output: Dict[str, Any]

@router.get("/", response_model=List[InferenceRecordSchema])
def list_inferences():
    """Returns all cryptographically signed inference records in the vault."""
    return list(INFERENCE_STORE.values())

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

@router.post("/reset")
def reset_inferences():
    """Resets all inference records and Merkle leaves back to original clean cryptographic baseline."""
    global INFERENCE_STORE, MERKLE_LEAVES
    INFERENCE_STORE.clear()
    MERKLE_LEAVES.clear()
    seed_demo_records()
    return {"status": "success", "message": "Inference vault reset to pristine cryptographic state."}

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
