import cv2
import numpy as np
from skimage.feature import local_binary_pattern

def extract_color_histogram(image_path: str, bins=(8, 8, 8)) -> np.ndarray:
    """Extracts a 3D color histogram from an image."""
    image = cv2.imread(image_path)
    if image is None:
        return np.zeros(bins[0]*bins[1]*bins[2])
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    hist = cv2.calcHist([image], [0, 1, 2], None, bins, [0, 256, 0, 256, 0, 256])
    cv2.normalize(hist, hist)
    return hist.flatten()

def extract_lbp(image_path: str, num_points=24, radius=3) -> np.ndarray:
    """Extracts Local Binary Pattern (LBP) histogram (texture)."""
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if image is None:
        return np.zeros(num_points + 2)
    lbp = local_binary_pattern(image, num_points, radius, method="uniform")
    (hist, _) = np.histogram(lbp.ravel(), bins=np.arange(0, num_points + 3), range=(0, num_points + 2))
    hist = hist.astype("float")
    hist /= (hist.sum() + 1e-7)
    return hist
