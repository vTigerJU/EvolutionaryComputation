import random
import time
import copy

maximum_generation = 500

def random_solution(size):
    """Creates a "board" of size n with no vertical or horizontal collisions"""
    node = list(range(size))
    random.shuffle(node)
    return node

def count_conflicts(node):
    d1, d2, rows = {}, {}, {}
    for c, r in enumerate(node):
        d1[c - r] = d1.get(c - r, 0) + 1 
        d2[c + r] = d2.get(c + r, 0) + 1
        rows[r] = rows.get(r, 0) + 1     
    conf = 0
    for k in d1.values():
        if k > 1: conf += k*(k-1)//2
    for k in d2.values():
        if k > 1: conf += k*(k-1)//2
    for k in rows.values():
        if k > 1: conf += k*(k-1)//2
    return conf

def tournamentSelection2(population, tournamentSize):
    """Returns Best state out of n random choices"""
    size = len(population)
    ixList = sorted(random.sample(range(size), tournamentSize))
    return population[ixList[0]], population[ixList[1]]

def rankingSelection(population):
    """Linear ranking selection y = 0 -> i=20"""
    m = 0.8
    k = -0.04
    for i in range(len(population)):
        if k*i + m  <= 0:
            return population[i]
        if random.random() < (k*i + m):
            return population[i]

def tournamentPicking(population, elitism,crossover_rate):
    """Crossover using tournament selection"""
    size_elitism = int(len(population) * elitism)
    new_population = population[:size_elitism] #Keep top n%
    tournamentSize = 20

    while len(new_population) < len(population):
        if random.random() < crossover_rate:
            parentA, parentB = tournamentSelection2(population[:size_elitism], tournamentSize)
            child = crossover_twopoint(parentA, parentB)
            new_population.append(child)
        else:
            #If crossover doesn't happen mutate random in top x%
            parentA = random.choice(population[:size_elitism])[:]
            new_population.append(mutate(parentA))
    return new_population[: len(population)]

def crossover_twopoint(nodeA, nodeB):
    """Crossover between two random points in list"""
    size = len(nodeA)
    ix1, ix2 = sorted(random.sample(range(size), 2))
    
    child = nodeA[:ix1] + nodeB[ix1:ix2] + nodeA[ix2:]
    return child

def mutate(node):
    """Mutation by switching two columns"""
    i, j = random.sample(range(len(node)), 2)
    node[i], node[j] = node[j], node[i]
    return node

def solve(n_size, population_size,crossover_rate):
    start = time.time()
    population = [random_solution(n_size) for _ in range(population_size)]
    elitism = 0.1
    for generation in range(maximum_generation):
        population.sort(key=count_conflicts)
        best = population[0]
        if count_conflicts(best) == 0:
            elapsed = time.time() - start
            return {
                "n": n_size,
                "gen": generation,
                "time_s": elapsed,
                "found": True,
            }
        
        population = tournamentPicking(population,elitism,crossover_rate)

        if generation + 1 == maximum_generation:
            elapsed = time.time() - start
            return {
                "n": n_size,
                "gen": generation,
                "time_s": elapsed,
                "found": False,
            }