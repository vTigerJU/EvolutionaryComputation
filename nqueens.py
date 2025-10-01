import random
import time
from inversion import inversion_mutate

maximum_generation = 1000
population_size = 260
mutation_rate = 0.2
crossover_rate = 0.2
inversion_rate = 0.15


def random_solution(size):
    """Creates a "board" of size n with no vertical or horizontal collisions
    index -> column
    value at index i -> row
    """
    node = list(range(size))
    random.shuffle(node)
    return node


def count_conflicts(node):
    """Count the conflicts between queens"""
    n = len(node)  # Size of board
    count = 0  # Collision count
    for ix in range(n):  # Check diagonal from left to right
        for j in range(ix + 1, n):
            if node[ix] == node[j]:
                count += 1
            if abs(ix - j) == abs(node[ix] - node[j]):  # if column diff == row diff
                count += 1
    return count

def count_conflicts_fast(node):
    d1, d2 = {}, {}
    for c, r in enumerate(node):
        d1[c - r] = d1.get(c - r, 0) + 1
        d2[c + r] = d2.get(c + r, 0) + 1
    conf = 0
    for k in d1.values():
        if k > 1: conf += k*(k-1)//2
    for k in d2.values():
        if k > 1: conf += k*(k-1)//2
    return conf

def crossover(nodeA, nodeB):
    """Swaps last half from each node"""
    mid = len(nodeA) // 2
    nodeA_back = nodeA[mid:]
    nodeB_back = nodeB[mid:]
    nodeA = nodeA[:mid] + nodeB_back
    nodeB = nodeB[:mid] + nodeA_back

    return nodeA, nodeB

#paper based crossover
def crossover_twopoint(nodeA, nodeB):
    """Swaps segments between two points from each node"""
    size = len(nodeA)
    point1 = random.randint(0, size - 1)
    point2 = random.randint(0, size - 1)
    if point1 > point2:
        point1, point2 = point2, point1

    # Create children with None values
    childA = [None] * size
    childB = [None] * size

    # Copy the segment from parents to children
    childA[point1:point2] = nodeA[point1:point2]
    childB[point1:point2] = nodeB[point1:point2]

    # Fill in the remaining positions
    def fill_child(child, parent):
        current_pos = point2 % size
        for value in parent:
            if value not in child:
                child[current_pos] = value
                current_pos = (current_pos + 1) % size

    fill_child(childA, nodeB)
    fill_child(childB, nodeA)

    return childA, childB


def mutate(node):
    i, j = random.sample(range(len(node)), 2)
    node[i], node[j] = node[j], node[i]

    inversion_mutate(node, rate=inversion_rate)


def repair(node):
    rows = set(range(len(node)))
    for i in range(len(node)):
        if node[i] not in rows:
            node[i] = random.choice(list(rows))
        rows.remove(node[i])
    return node


def solve(n_size, do_crossover):
    start = time.time()
    population = [random_solution(n_size) for _ in range(population_size)]

    for generation in range(maximum_generation):
        population.sort(key=count_conflicts_fast)
        best = population[0]
        if count_conflicts_fast(best) == 0:
            elapsed = time.time() - start
            return {
                "n": n_size,
                "gen": generation,
                "time_s": elapsed,
                # "solution": best,
                "found": True,
            }

        new_pop = population[:10]
     
        while len(new_pop) < population_size:
            parent = random.choice(population[:15])[:]
            mutate(parent)
            new_pop.append(parent)

        population = new_pop

        if generation + 1 == maximum_generation:
            return count_conflicts(best)


if __name__ == "__main__":
    for i in range(20):
        print(solve(200, False))