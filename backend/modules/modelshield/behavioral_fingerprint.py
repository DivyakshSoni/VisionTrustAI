import torch
import numpy as np
import hashlib
from typing import List, Callable, Any

def generate_behavioral_fingerprint(model_inference_fn: Callable[[Any], np.ndarray], probe_dataset: List[Any]) -> str:
    """
    Runs a fixed probe-image battery through the model, vectorizes the output distributions,
    and computes a SHA-256 hash. Works for black-box models (e.g. ONNX).
    """
    outputs = []
    
    for probe_input in probe_dataset:
        # Expected to return probabilities or logits as numpy array
        output = model_inference_fn(probe_input) 
        outputs.append(output.flatten())
        
    # Concatenate all outputs into one large vector
    full_vector = np.concatenate(outputs)
    
    # Quantize slightly to avoid floating point differences between machines/runs
    # Round to 4 decimal places
    quantized_vector = np.round(full_vector, decimals=4)
    
    # Hash the bytes of the vector
    vector_bytes = quantized_vector.tobytes()
    return hashlib.sha256(vector_bytes).hexdigest()

def verify_fingerprint(model_inference_fn: Callable[[Any], np.ndarray], probe_dataset: List[Any], reference_fingerprint: str) -> bool:
    """
    Verifies the model's behavioral fingerprint against a reference.
    """
    computed_fingerprint = generate_behavioral_fingerprint(model_inference_fn, probe_dataset)
    return computed_fingerprint == reference_fingerprint
