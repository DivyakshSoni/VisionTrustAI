from backend.core.crypto.hashing import hash_file
import os

def verify_model_digest(model_path: str, expected_digest: str) -> bool:
    """
    Hashes the model weights and compares the computed digest against the declared digest.
    """
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model file not found: {model_path}")
        
    computed_digest = hash_file(model_path)
    return computed_digest == expected_digest
