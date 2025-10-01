import random

# hypothesis: higher population size => lower gens (more computer power required)

def inversion_mutate(node: list[int], rate: float = 0.05) -> None:
    """Apply smart inversion mutation targeting diagonal conflicts.
    
    Strategy: Find queens involved in diagonal conflicts and try to break
    diagonal patterns by inverting segments that contain conflicted queens.
    """
    if len(node) < 3:  # Need at least 3 elements for meaningful inversion
        return
    if random.random() >= rate:
        return
    
    n = len(node)
    
    # Strategy 1: Target diagonal streaks (most common problem)
    if random.random() < 0.6:  # 60% chance to use diagonal targeting
        _invert_diagonal_streaks(node, n)
    else:
        #Strategy 2: Multi-segment inversion for diversity
        _invert_multiple_segments(node, n)


def _invert_diagonal_streaks(node: list[int], n: int) -> None:
    """Find and invert segments that form diagonal patterns."""
    #Look for consecutive elements that form diagonal patterns
    
    best_start = None
    best_end = None
    max_streak = 0
    
    # Check for ascending diagonal streaks (i + node[i] = constant)
    for i in range(n - 1):
        if node[i + 1] == node[i] + 1:  # Ascending diagonal
            start = i
            end = i + 1
            # Extend the streak
            while end < n and node[end] == node[end - 1] + 1:
                end += 1
            if end - start > max_streak:
                max_streak = end - start
                best_start = start
                best_end = end
    
    # Check for descending diagonal streaks (i - node[i] = constant)
    for i in range(n - 1):
        if node[i + 1] == node[i] - 1:  # Descending diagonal
            start = i
            end = i + 1
            # Extend the streak
            while end < n and node[end] == node[end - 1] - 1:
                end += 1
            if end - start > max_streak:
                max_streak = end - start
                best_start = start
                best_end = end
    
    # If we found a diagonal streak, invert it
    if best_start is not None and best_end - best_start >= 2:
        node[best_start:best_end] = reversed(node[best_start:best_end])
    else:
        # Fallback: random inversion
        start, end = sorted(random.sample(range(n), 2))
        if end - start >= 2:
            node[start:end] = reversed(node[start:end])


def _invert_multiple_segments(node: list[int], n: int) -> None:
    """Apply multiple small inversions for diversity."""
    num_inversions = random.randint(1, min(3, n // 10 + 1))
    
    for _ in range(num_inversions):
        # Pick segment size based on board size
        if n <= 20:
            min_size = 2
            max_size = min(5, n // 3)
        elif n <= 100:
            min_size = 3
            max_size = min(8, n // 5)
        else:  # n > 100
            min_size = 4
            max_size = min(12, n // 8)
        
        if max_size < min_size:
            max_size = min_size
        
        segment_size = random.randint(min_size, max_size)
        start = random.randint(0, n - segment_size)
        end = start + segment_size
        
        node[start:end] = reversed(node[start:end])


