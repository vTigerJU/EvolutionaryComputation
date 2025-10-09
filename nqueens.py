import random
import time
from inversion import inversion_mutate

maximum_generation = 1000

def random_solution(size):
    """Creates a "board" of size n with no vertical or horizontal collisions"""
    node = list(range(size))
    random.shuffle(node)
    return node

def count_conflicts_fast(node):
    d1, d2 = {}, {}
    for c, r in enumerate(node): #Counts queens on both diagonals
        d1[c - r] = d1.get(c - r, 0) + 1
        d2[c + r] = d2.get(c + r, 0) + 1
    conf = 0
    for k in d1.values():
        if k > 1: conf += k*(k-1)//2
    for k in d2.values():
        if k > 1: conf += k*(k-1)//2
    return conf

def mutate(node, inversion_rate):
    """Swaps the position of two random queens"""
    i, j = random.sample(range(len(node)), 2)
    node[i], node[j] = node[j], node[i]

    inversion_mutate(node, rate=inversion_rate) 

def solve_track_generation(n_size, population_size, inversion_rate):
    population = [random_solution(n_size) for _ in range(population_size)] #Fill population with random solutions
    best_fitness = []
    for generation in range(maximum_generation): #Iterating over generations
        population.sort(key=count_conflicts_fast) #Sort population
        best = population[0] #Solution with the least conflicts
        best_fitness.append(count_conflicts_fast(best))
        if count_conflicts_fast(best) == 0: #Solution found
            return best_fitness

        new_pop = population[:10] #Keep 10 best solutions
     
        while len(new_pop) < population_size: #Fill out the new population with mutations
            parent = random.choice(population[:15])[:] #Mutate top 15
            mutate(parent, inversion_rate)
            new_pop.append(parent)

        population = new_pop

        if generation + 1 == maximum_generation:
            return best_fitness

def solve(n_size, population_size, inversion_rate):
    start = time.time()
    population = [random_solution(n_size) for _ in range(population_size)] #Fill population with random solutions

    for generation in range(maximum_generation): #Iterating over generations
        population.sort(key=count_conflicts_fast) #Sort population
        best = population[0] #Solution with the least conflicts
        if count_conflicts_fast(best) == 0: #Solution found
            elapsed = time.time() - start
            return {
                "n": n_size,
                "gen": generation,
                "time_s": elapsed,
                "found": True,
            }

        new_pop = population[:10] #Keep 10 best solutions
     
        while len(new_pop) < population_size: #Fill out the new population with mutations
            parent = random.choice(population[:15])[:] #Mutate top 15
            mutate(parent, inversion_rate)
            new_pop.append(parent)

        population = new_pop

        if generation + 1 == maximum_generation:
            elapsed = time.time() - start
            return {
                "n": n_size,
                "gen": generation,
                "time_s": elapsed,
                "found": False,
            }


if __name__ == "__main__":
    for i in range(20):
        print(solve(200, False))