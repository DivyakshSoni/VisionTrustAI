from cryptography.hazmat.primitives.asymmetric import ed25519
from backend.core.crypto.hashing import hash_record
from backend.core.crypto.signing import verify_signature
from backend.core.schemas.schemas import InferenceRecordSchema
from backend.core.crypto.merkle import MerkleTree

def verify_inference_record(
    record: InferenceRecordSchema, 
    public_key: ed25519.Ed25519PublicKey, 
    merkle_tree: MerkleTree = None
) -> bool:
    """
    Re-checks the hash, signature, and optionally the Merkle path.
    """
    ts = record.timestamp
    if not isinstance(ts, str):
        ts = ts.isoformat().replace("+00:00", "") + "Z"

    recomputed_hash = hash_record(
        input_hash=record.input_hash,
        model_digest=record.model_digest,
        preproc_hash=record.preprocessing_config_hash,
        inf_hash=record.inference_config_hash,
        output=record.output,
        timestamp=ts,
        nonce=record.sequence_nonce
    )
    
    if recomputed_hash != record.record_hash:
        return False
        
    # 2. Verify signature
    try:
        sig_bytes = bytes.fromhex(record.signature)
    except ValueError:
        return False
        
    is_valid_sig = verify_signature(public_key, sig_bytes, record.record_hash.encode('utf-8'))
    
    if not is_valid_sig:
        return False
        
    # 3. Verify Merkle Path (if tree provided)
    if merkle_tree:
        return merkle_tree.verify_record(record.record_hash)
        
    return True
