import hashlib
import json
from typing import Dict, Any

def hash_data(data: bytes) -> str:
    """Computes SHA-256 hash of raw bytes."""
    return hashlib.sha256(data).hexdigest()

def hash_file(filepath: str) -> str:
    """Computes SHA-256 hash of a file (useful for images or model weights)."""
    sha256_hash = hashlib.sha256()
    with open(filepath, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def hash_config(config: Dict[str, Any]) -> str:
    """Computes SHA-256 hash of a configuration dictionary."""
    config_str = json.dumps(config, sort_keys=True).encode('utf-8')
    return hash_data(config_str)

def hash_record(input_hash: str, model_digest: str, preproc_hash: str, inf_hash: str, output: Any, timestamp: str, nonce: str) -> str:
    """Computes a composite hash for an InferenceRecord."""
    record_dict = {
        "input_hash": input_hash,
        "model_digest": model_digest,
        "preprocessing_config_hash": preproc_hash,
        "inference_config_hash": inf_hash,
        "output": output,
        "timestamp": timestamp,
        "sequence_nonce": nonce
    }
    return hash_config(record_dict)
