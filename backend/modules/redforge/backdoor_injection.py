import cv2
import os
import random
from typing import List, Dict

def apply_synthetic_trigger(image_path: str, out_path: str, patch_size: int = 10):
    """
    Applies a small fixed-pixel white square (trigger) to the bottom right of the image.
    """
    img = cv2.imread(image_path)
    if img is None:
        return False
        
    h, w, _ = img.shape
    # Draw a white patch in the bottom right corner
    start_y = max(0, h - patch_size - 5)
    start_x = max(0, w - patch_size - 5)
    
    img[start_y:start_y+patch_size, start_x:start_x+patch_size] = (255, 255, 255)
    cv2.imwrite(out_path, img)
    return True

def inject_backdoor_triggers(dataset: List[Dict], target_label: str, target_dir: str, injection_rate: float = 0.05) -> Dict:
    """
    Injects a synthetic patch into a subset of images and relabels them to the target_label.
    """
    os.makedirs(target_dir, exist_ok=True)
    
    num_to_inject = int(len(dataset) * injection_rate)
    indices = random.sample(range(len(dataset)), num_to_inject)
    
    manifest = []
    poisoned_dataset = [dict(item) for item in dataset]
    
    for idx in indices:
        original_entry = dataset[idx]
        src_path = original_entry.get("image_path")
        
        if not src_path or not os.path.exists(src_path):
            continue
            
        filename = f"bd_{os.path.basename(src_path)}"
        out_path = os.path.join(target_dir, filename)
        
        if apply_synthetic_trigger(src_path, out_path):
            poisoned_dataset[idx]["image_path"] = out_path
            poisoned_dataset[idx]["label"] = target_label
            
            manifest.append({
                "index": idx,
                "original_path": src_path,
                "poisoned_path": out_path,
                "original_label": original_entry.get("label"),
                "new_label": target_label
            })
            
    return {
        "poisoned_dataset": poisoned_dataset,
        "manifest": manifest,
        "attack_type": "backdoor_injection"
    }
