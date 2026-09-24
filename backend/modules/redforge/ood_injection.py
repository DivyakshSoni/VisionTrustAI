import random
from typing import List, Dict

def inject_ood_samples(dataset: List[Dict], ood_image_paths: List[str], target_labels: List[str], injection_rate: float = 0.05) -> Dict:
    """
    Inserts out-of-distribution (OOD) images into the dataset and assigns them target labels.
    """
    num_to_inject = int(len(dataset) * injection_rate)
    inject_paths = random.sample(ood_image_paths, min(num_to_inject, len(ood_image_paths)))
    
    manifest = []
    poisoned_dataset = [dict(item) for item in dataset]
    
    for path in inject_paths:
        target_label = random.choice(target_labels)
        
        new_entry = {
            "image_path": path,
            "label": target_label,
            "is_ood": True
        }
        poisoned_dataset.append(new_entry)
        
        manifest.append({
            "injected_path": path,
            "assigned_label": target_label
        })
        
    return {
        "poisoned_dataset": poisoned_dataset,
        "manifest": manifest,
        "attack_type": "ood_injection"
    }
