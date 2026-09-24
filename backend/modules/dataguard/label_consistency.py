from sklearn.neighbors import NearestNeighbors
import numpy as np

def check_label_consistency(embeddings: np.ndarray, labels: list, k: int = 5) -> list:
    """
    Checks if a sample's label is consistent with its k-nearest neighbors in embedding space.
    Returns a list of suspicious indices where the label disagrees with the majority.
    """
    if len(embeddings) < k + 1:
        return []

    nbrs = NearestNeighbors(n_neighbors=k+1, algorithm='ball_tree').fit(embeddings)
    distances, indices = nbrs.kneighbors(embeddings)
    
    suspicious = []
    for i, neighbors in enumerate(indices):
        # Exclude the point itself (usually the first neighbor)
        neighbor_labels = [labels[idx] for idx in neighbors[1:]]
        majority_label = max(set(neighbor_labels), key=neighbor_labels.count)
        
        if labels[i] != majority_label:
            suspicious.append({
                "index": i,
                "assigned_label": labels[i],
                "majority_neighbor_label": majority_label
            })
            
    return suspicious
