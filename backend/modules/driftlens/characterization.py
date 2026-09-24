import cv2
import numpy as np
from typing import List, Dict, Any

def compute_average_brightness(image_path: str) -> float:
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        return 0.0
    return float(np.mean(img))

def characterize_drift(ref_paths: List[str], new_paths: List[str]) -> Dict[str, Any]:
    """
    Compares simple visual statistics (like brightness) to help explain 
    an observed distribution shift (Drift vs Attack).
    """
    ref_brightness = [compute_average_brightness(p) for p in ref_paths]
    new_brightness = [compute_average_brightness(p) for p in new_paths]
    
    ref_mean = np.mean(ref_brightness) if ref_brightness else 0
    new_mean = np.mean(new_brightness) if new_brightness else 0
    
    diff = new_mean - ref_mean
    
    explanation = "No significant brightness change."
    if diff > 20:
        explanation = "Incoming batch is significantly brighter. Possible illumination drift (e.g. daytime vs nighttime or over-exposure)."
    elif diff < -20:
        explanation = "Incoming batch is significantly darker. Possible illumination drift."
        
    return {
        "reference_mean_brightness": ref_mean,
        "new_mean_brightness": new_mean,
        "difference": diff,
        "explanation": explanation
    }
