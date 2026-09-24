import uuid
import datetime
import secrets
from typing import Dict, Any

from backend.core.crypto.hashing import hash_record, hash_data
from backend.core.crypto.signing import sign_data
from cryptography.hazmat.primitives.asymmetric import ed25519
from backend.core.schemas.schemas import InferenceRecordSchema

def create_inference_record(
    input_hash: str,
    model_digest: str,
    preprocessing_config_hash: str,
    inference_config_hash: str,
    output: Dict[str, Any],
    private_key: ed25519.Ed25519PrivateKey
) -> InferenceRecordSchema:
    """
    Creates a cryptographically bound and signed InferenceRecord.
    """
    record_id = f"INF-{uuid.uuid4().hex[:8].upper()}"
    timestamp = datetime.datetime.utcnow().isoformat() + "Z"
    sequence_nonce = secrets.token_hex(16)
    
    # Compute the composite hash for the record
    rec_hash = hash_record(
        input_hash=input_hash,
        model_digest=model_digest,
        preproc_hash=preprocessing_config_hash,
        inf_hash=inference_config_hash,
        output=output,
        timestamp=timestamp,
        nonce=sequence_nonce
    )
    
    # Sign the record hash
    signature_bytes = sign_data(private_key, rec_hash.encode('utf-8'))
    signature_hex = signature_bytes.hex()
    
    return InferenceRecordSchema(
        record_id=record_id,
        input_hash=input_hash,
        model_digest=model_digest,
        preprocessing_config_hash=preprocessing_config_hash,
        inference_config_hash=inference_config_hash,
        output=output,
        timestamp=timestamp,
        sequence_nonce=sequence_nonce,
        record_hash=rec_hash,
        signature=signature_hex,
        crypto_verified=True
    )
