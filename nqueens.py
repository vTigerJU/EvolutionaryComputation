import random
import time

maximum_generation = 300
population_size = 200
mutation_rate = 0.2
crossover_rate = 0.2


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
    """Mutation by switching two columns"""
    i, j = random.sample(range(len(node)), 2)
    node[i], node[j] = node[j], node[i]
    

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
        population.sort(key=count_conflicts)
        best = population[0]
        if count_conflicts(best) == 0:
            elapsed = time.time() - start
            return {
                "n": n_size,
                "gen": generation,
                "time_s": elapsed,
                # "solution": best,
                "found": True,
            }

        new_pop = population[:50]
        if do_crossover:
            for i in range(20):
                nodeA, nodeB = crossover(new_pop[i], new_pop[i * 2])
                new_pop.append(nodeA)
                new_pop.append(nodeB)
        while len(new_pop) < population_size:
            parent = random.choice(population[:50])[:]
            mutate(parent)
            new_pop.append(parent)

        population = new_pop

        if generation + 1 == maximum_generation:
            return count_conflicts(best)


if __name__ == "__main__":
    for i in range(20):
        print(solve(80, False))
    print("crossover")
    for i in range(20):
        print(solve(80, True))
