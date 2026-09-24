import random
from typing import List, Dict

def inject_label_flips(dataset: List[Dict], flip_rate: float = 0.1, available_labels: List[str] = None) -> Dict:
    """
    Randomly flips a percentage of labels in the dataset.
    Returns the modified dataset and a ground-truth manifest of altered samples.
    """
    if not available_labels:
        available_labels = list(set([item.get("label") for item in dataset if "label" in item]))
        
    num_to_flip = int(len(dataset) * flip_rate)
    indices_to_flip = random.sample(range(len(dataset)), num_to_flip)
    
    manifest = []
    poisoned_dataset = [dict(item) for item in dataset] # shallow copy
    
    for idx in indices_to_flip:
        original_label = poisoned_dataset[idx].get("label")
        possible_new_labels = [lbl for lbl in available_labels if lbl != original_label]
        new_label = random.choice(possible_new_labels) if possible_new_labels else original_label
        
        poisoned_dataset[idx]["label"] = new_label
        manifest.append({
            "index": idx,
            "original_label": original_label,
            "new_label": new_label
        })
        
    return {
        "poisoned_dataset": poisoned_dataset,
        "manifest": manifest,
        "attack_type": "label_flip"
    }
