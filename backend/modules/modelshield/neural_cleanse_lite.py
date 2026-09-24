import torch
import torch.nn as nn
import torch.optim as optim
from typing import Dict, Tuple

def analyze_class_trigger(model: nn.Module, data_loader, target_class: int, img_shape: Tuple[int, int, int], device: str = "cpu", epochs: int = 5) -> float:
    """
    Optimizes a mask and pattern to force misclassification to the target_class.
    Returns the L1 norm of the optimized mask. A very small mask indicates a potential backdoor.
    """
    model.eval()
    
    # Initialize mask and pattern as learnable parameters
    mask = torch.rand((1, img_shape[1], img_shape[2]), requires_grad=True, device=device)
    pattern = torch.rand(img_shape, requires_grad=True, device=device)
    
    optimizer = optim.Adam([mask, pattern], lr=0.1)
    criterion = nn.CrossEntropyLoss()
    
    for epoch in range(epochs):
        for inputs, _ in data_loader:
            inputs = inputs.to(device)
            
            optimizer.zero_grad()
            
            # constrain mask and pattern
            m = torch.clamp(mask, 0.0, 1.0)
            p = torch.clamp(pattern, 0.0, 1.0)
            
            # Apply trigger: (1 - m) * x + m * p
            poisoned_inputs = (1 - m) * inputs + m * p
            
            outputs = model(poisoned_inputs)
            targets = torch.full((inputs.size(0),), target_class, dtype=torch.long, device=device)
            
            # Loss: Classification loss + Regularization on mask size (L1 norm)
            loss_cls = criterion(outputs, targets)
            loss_reg = torch.sum(torch.abs(m))
            
            # Weighting factor for regularization (lambda)
            loss = loss_cls + 0.01 * loss_reg
            
            loss.backward()
            optimizer.step()
            
    final_mask = torch.clamp(mask, 0.0, 1.0).detach()
    mask_size = torch.sum(torch.abs(final_mask)).item()
    return mask_size

def run_neural_cleanse_lite(model: nn.Module, data_loader, num_classes: int, img_shape: Tuple[int, int, int], device: str = "cpu") -> Dict[int, float]:
    """
    Runs trigger optimization for all classes and compares mask sizes.
    Returns a dictionary of class_idx -> mask_size.
    """
    # Check white-box access
    if not isinstance(model, nn.Module) or not any(p.requires_grad for p in model.parameters()):
        raise ValueError("Neural Cleanse Lite requires a PyTorch model with gradients (White-box access).")
        
    mask_sizes = {}
    for c in range(num_classes):
        mask_sizes[c] = analyze_class_trigger(model, data_loader, c, img_shape, device)
        
    return mask_sizes
