from sklearn.cluster import KMeans
import numpy as np
from typing import Dict, List

def detect_poisoning_clusters(activations_by_class: Dict[str, np.ndarray]) -> List[Dict]:
    """
    Given penultimate-layer activations grouped by class, runs k-means (k=2) to find
    suspicious tight sub-clusters indicative of backdoor poisoning.
    """
    findings = []
    
    for cls_name, activations in activations_by_class.items():
        if len(activations) < 10:
            continue
            
        kmeans = KMeans(n_clusters=2, random_state=42, n_init=10).fit(activations)
        labels = kmeans.labels_
        
        # Check size of clusters
        c0_size = np.sum(labels == 0)
        c1_size = np.sum(labels == 1)
        
        # If one cluster is very small compared to the other, it might be an injected trigger cluster
        ratio = min(c0_size, c1_size) / max(c0_size, c1_size)
        
        if ratio < 0.15: # e.g., less than 15% of the data
            small_cluster_label = 0 if c0_size < c1_size else 1
            small_cluster_indices = np.where(labels == small_cluster_label)[0].tolist()
            findings.append({
                "class": cls_name,
                "suspicious_indices": small_cluster_indices,
                "reason": "Tight anomalous sub-cluster detected."
            })
            
    return findings
