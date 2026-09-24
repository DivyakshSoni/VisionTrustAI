import torch

def compute_rbf_kernel(x: torch.Tensor, y: torch.Tensor, sigma: float = 1.0) -> torch.Tensor:
    """Computes the RBF (Gaussian) kernel between two sets of tensors."""
    x_size = x.size(0)
    y_size = y.size(0)
    dim = x.size(1)

    x = x.unsqueeze(1).expand(x_size, y_size, dim)
    y = y.unsqueeze(0).expand(x_size, y_size, dim)
    
    return torch.exp(-((x - y) ** 2).sum(2) / (2 * sigma ** 2))

def compute_mmd(ref_embeddings: torch.Tensor, new_embeddings: torch.Tensor, sigma: float = 1.0) -> float:
    """
    Computes Maximum Mean Discrepancy (MMD) between a reference distribution 
    and a new distribution using an RBF kernel.
    """
    xx = compute_rbf_kernel(ref_embeddings, ref_embeddings, sigma)
    yy = compute_rbf_kernel(new_embeddings, new_embeddings, sigma)
    xy = compute_rbf_kernel(ref_embeddings, new_embeddings, sigma)
    
    return xx.mean().item() + yy.mean().item() - 2 * xy.mean().item()
