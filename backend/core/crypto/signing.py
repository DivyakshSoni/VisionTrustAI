from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.primitives import serialization
from typing import Tuple

def generate_keypair() -> Tuple[ed25519.Ed25519PrivateKey, ed25519.Ed25519PublicKey]:
    """Generates an Ed25519 keypair."""
    private_key = ed25519.Ed25519PrivateKey.generate()
    public_key = private_key.public_key()
    return private_key, public_key

def sign_data(private_key: ed25519.Ed25519PrivateKey, data: bytes) -> bytes:
    """Signs raw bytes using Ed25519."""
    return private_key.sign(data)

def verify_signature(public_key: ed25519.Ed25519PublicKey, signature: bytes, data: bytes) -> bool:
    """Verifies an Ed25519 signature."""
    try:
        public_key.verify(signature, data)
        return True
    except Exception:
        return False

def serialize_public_key(public_key: ed25519.Ed25519PublicKey) -> bytes:
    """Serializes the public key to PEM format."""
    return public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

def deserialize_public_key(pem_data: bytes) -> ed25519.Ed25519PublicKey:
    """Loads a public key from PEM format."""
    return serialization.load_pem_public_key(pem_data)
