import numpy as np

def calculate_psi(expected: np.ndarray, actual: np.ndarray, buckets: int = 10) -> float:
    """
    Computes Population Stability Index (PSI) between two 1D numerical arrays.
    """
    # Define bucket edges based on expected distribution
    breakpoints = np.percentile(expected, np.linspace(0, 100, buckets + 1))
    # Avoid zero-width bins
    breakpoints = np.unique(breakpoints)
    if len(breakpoints) < 2:
        return 0.0

    # Count samples in buckets
    expected_counts, _ = np.histogram(expected, bins=breakpoints)
    actual_counts, _ = np.histogram(actual, bins=breakpoints)
    
    # Convert to fractions
    expected_fracs = expected_counts / len(expected)
    actual_fracs = actual_counts / len(actual)
    
    # Replace zeros with a small epsilon to avoid division by zero or log(0)
    epsilon = 1e-6
    expected_fracs = np.where(expected_fracs == 0, epsilon, expected_fracs)
    actual_fracs = np.where(actual_fracs == 0, epsilon, actual_fracs)
    
    # Calculate PSI
    psi_values = (actual_fracs - expected_fracs) * np.log(actual_fracs / expected_fracs)
    return float(np.sum(psi_values))

def evaluate_psi(psi_score: float) -> str:
    """Standard rule-of-thumb interpretation of PSI."""
    if psi_score < 0.1:
        return "No significant drift"
    elif psi_score < 0.2:
        return "Moderate drift"
    else:
        return "Significant drift"
