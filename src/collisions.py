from dataclasses import dataclass

@dataclass
class CollisionGroup:
    diagonal: str        # '\' or '/'
    diag_id: int         # row-col (for '\') or row+col (for '/')
    queens: list         # list of (row, col) tuples
    
    def num_conflicts(self):
        k = len(self.queens)
        return k * (k - 1) // 2
    
        