import random
from PIL import Image, ImageEnhance
import os
from typing import List, Dict

def inject_duplicate_flood(image_paths: List[str], target_dir: str, num_copies: int = 5, flood_rate: float = 0.05) -> Dict:
    """
    Takes a random sample of images and inserts near-identical copies using augmentations.
    Returns the paths of the new images and a ground-truth manifest.
    """
    os.makedirs(target_dir, exist_ok=True)
    
    num_to_flood = int(len(image_paths) * flood_rate)
    indices_to_flood = random.sample(range(len(image_paths)), num_to_flood)
    
    manifest = []
    generated_paths = []
    
    for idx in indices_to_flood:
        src_path = image_paths[idx]
        try:
            img = Image.open(src_path)
            
            for copy_idx in range(num_copies):
                # Apply slight brightness jitter to simulate near-duplicate
                enhancer = ImageEnhance.Brightness(img)
                jittered = enhancer.enhance(random.uniform(0.8, 1.2))
                
                filename = f"flood_{idx}_{copy_idx}_{os.path.basename(src_path)}"
                out_path = os.path.join(target_dir, filename)
                jittered.save(out_path)
                generated_paths.append(out_path)
                
                manifest.append({
                    "original_source": src_path,
                    "generated_copy": out_path,
                    "augmentation": "brightness_jitter"
                })
        except Exception as e:
            print(f"Failed to process {src_path}: {e}")
            
    return {
        "generated_paths": generated_paths,
        "manifest": manifest,
        "attack_type": "duplicate_flood"
    }
