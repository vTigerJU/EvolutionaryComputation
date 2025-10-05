import random
import time
from inversion import inversion_mutate

maximum_generation = 1000

def random_solution(size):
    """Creates a "board" of size n with no vertical or horizontal collisions
    index -> column
    value at index i -> row
    """
    node = list(range(size))
    random.shuffle(node)
    return node

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

def mutate(node, inversion_rate):
    i, j = random.sample(range(len(node)), 2)
    node[i], node[j] = node[j], node[i]

    inversion_mutate(node, rate=inversion_rate)

def solve(n_size, population_size, inversion_rate):
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
            mutate(parent, inversion_rate)
            new_pop.append(parent)

        population = new_pop

        if generation + 1 == maximum_generation:
            return count_conflicts_fast(best)


if __name__ == "__main__":
    for i in range(20):
        print(solve(200, False))