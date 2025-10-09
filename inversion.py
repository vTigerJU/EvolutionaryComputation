import random


def inversion_mutate(node: list[int], rate: float = 0.05) -> None:
    if len(node) < 3: 
        return
    if random.random() >= rate: #Returns if above inversion rate
        return
    
    n = len(node)
    
    if random.random() < 0.6:  #60% for diagonal invertion
        _invert_diagonal_streaks(node, n)
    else:
        _invert_multiple_segments(node, n)


def _invert_diagonal_streaks(node: list[int], n: int) -> None:
    best_start = None
    best_end = None
    max_streak = 0
    
    for i in range(n - 1): #Identifies longest descending streak of queens
        if node[i + 1] == node[i] + 1: 
            start = i
            end = i + 1
            while end < n and node[end] == node[end - 1] + 1:
                end += 1
            if end - start > max_streak:
                max_streak = end - start
                best_start = start
                best_end = end
    
    for i in range(n - 1): #Identifies longest ascending streak of queens
        if node[i + 1] == node[i] - 1: 
            start = i
            end = i + 1
            while end < n and node[end] == node[end - 1] - 1:
                end += 1
            if end - start > max_streak:
                max_streak = end - start
                best_start = start
                best_end = end
    
    #If longest chain >= 2 reverse it
    if best_start is not None and best_end - best_start >= 2:
        node[best_start:best_end] = reversed(node[best_start:best_end])
    else: #Invert random segment
        start, end = sorted(random.sample(range(n), 2))
        if end - start >= 2:
            node[start:end] = reversed(node[start:end])


def _invert_multiple_segments(node: list[int], n: int) -> None:
    num_inversions = random.randint(1, min(3, n // 10 + 1)) #Invert min 1-3 segments
    
    for _ in range(num_inversions): #Invert x random segments of length depending on n
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
        
        segment_size = random.randint(min_size, max_size) #Length of segment
        start = random.randint(0, n - segment_size) #Random start point
        end = start + segment_size
        
        node[start:end] = reversed(node[start:end]) 


