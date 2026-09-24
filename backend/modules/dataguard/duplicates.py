import imagehash
from PIL import Image
import torch
import torch.nn.functional as F

def compute_phash(image_path: str) -> str:
    """Computes perceptual hash of an image."""
    img = Image.open(image_path)
    return str(imagehash.phash(img))

def find_phash_duplicates(image_paths: list, threshold: int = 5) -> list:
    """Finds near-duplicates using pHash."""
    hashes = {}
    duplicates = []
    for path in image_paths:
        try:
            h = compute_phash(path)
            for existing_path, existing_hash in hashes.items():
                if abs(imagehash.hex_to_hash(h) - imagehash.hex_to_hash(existing_hash)) <= threshold:
                    duplicates.append((path, existing_path))
            hashes[path] = h
        except Exception:
            pass # Handle broken images gracefully
    return duplicates

def find_embedding_duplicates(embeddings: torch.Tensor, threshold: float = 0.98) -> list:
    """Finds near-duplicates using cosine similarity of embeddings (e.g. CLIP)."""
    normalized_embs = F.normalize(embeddings, p=2, dim=1)
    sim_matrix = torch.matmul(normalized_embs, normalized_embs.T)
    
    duplicates = []
    n = sim_matrix.size(0)
    for i in range(n):
        for j in range(i + 1, n):
            if sim_matrix[i, j].item() >= threshold:
                duplicates.append((i, j, sim_matrix[i, j].item()))
    return duplicates
