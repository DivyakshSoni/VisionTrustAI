from sklearn.ensemble import IsolationForest
import numpy as np

def detect_ood_isolation_forest(reference_embeddings: np.ndarray, new_embeddings: np.ndarray, contamination: float = 0.05) -> list:
    """
    Uses Isolation Forest fit on a reference distribution to detect out-of-distribution (OOD) samples.
    """
    clf = IsolationForest(contamination=contamination, random_state=42)
    clf.fit(reference_embeddings)
    
    predictions = clf.predict(new_embeddings)
    
    # IsolationForest returns -1 for anomalies, 1 for inliers
    ood_indices = np.where(predictions == -1)[0].tolist()
    scores = clf.score_samples(new_embeddings)
    
    return [{"index": int(idx), "anomaly_score": float(scores[idx])} for idx in ood_indices]
