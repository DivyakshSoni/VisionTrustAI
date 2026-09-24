import hashlib
from typing import List

def hash_pair(left: str, right: str) -> str:
    """Hashes a pair of node hashes."""
    combined = (left + right).encode('utf-8')
    return hashlib.sha256(combined).hexdigest()

class MerkleTree:
    """
    A simple offline-friendly Merkle tree for inference auditing.
    """
    def __init__(self, leaves: List[str]):
        self.leaves = leaves
        self.tree = self._build_tree(leaves)

    def _build_tree(self, leaves: List[str]) -> List[List[str]]:
        if not leaves:
            return []
        
        tree = [leaves]
        current_level = leaves

        while len(current_level) > 1:
            next_level = []
            for i in range(0, len(current_level), 2):
                left = current_level[i]
                right = current_level[i + 1] if i + 1 < len(current_level) else left
                next_level.append(hash_pair(left, right))
            tree.append(next_level)
            current_level = next_level

        return tree

    def get_root(self) -> str:
        if not self.tree:
            return ""
        return self.tree[-1][0]

    def verify_record(self, record_hash: str) -> bool:
        """
        Simple verification: checks if the hash exists in the leaves. 
        For full verification, a Merkle proof path would be generated and validated.
        """
        return record_hash in self.leaves
