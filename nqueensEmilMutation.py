import random
import time

maximum_generation = 2000
#population_size = 200
#mutation_rate = 0.2
#crossover_rate = 0.2
elite_frac = 0.04       # fraction of population preserved unchanged
parent_pool_frac = 0.07   # fraction of top population used for parent selection (must be >= elite_frac)


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

def mutate(node):
    """Mutation by switching two columns"""
    i, j = random.sample(range(len(node)), 2)
    node[i], node[j] = node[j], node[i]

def solve(n_size):
    population_size = int(n_size*1.3)
    start = time.time()
    population = [random_solution(n_size) for _ in range(population_size)]

     # derive counts from fractions (ensure at least 1 elite and parent pool >= elites)
    elite_k = max(1, int(round(elite_frac * population_size)))
    parent_k = max(elite_k, int(round(parent_pool_frac * population_size)))

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
                "elite_frac": elite_frac,
                "parent_pool_frac": parent_pool_frac
            }

        new_pop = population[:elite_k]
        while len(new_pop) < population_size:
            parent = random.choice(population[:parent_k])[:]
            mutate(parent)
            new_pop.append(parent)

        population = new_pop

        if generation + 1 == maximum_generation:
            return count_conflicts_fast(best)


if __name__ == "__main__":
    for i in range(10):
        print(solve(200))
    #print("crossover")
    #for i in range(20):
     #   print(solve(80, True))
