import random
import time
import copy

maximum_generation = 250
population_size = 250 #250+ gör ingen skillnad förutom extra tid eftersom den spetsar sig för tidigt
CROSSOVER_RATE = 0.8

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

def tournamentSelection(population, tournamentSize):
    """Returns Best state out of n random choices"""
    tournament = random.sample(population, tournamentSize)
    tournament.sort(key=count_conflicts)
    return tournament[0], tournament[1]

def tournamentSelection2(population, rankSize):
    size = len(population)
    ixList = sorted(random.sample(range(size), rankSize))
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

def tournamentPicking(population):
    """Crossover using tournament selection"""
    size = len(population) // 4
    new_population = population[:len(population) // 8 ] #Keep top n%
    tournamentSize = 20

    while len(new_population) < len(population):
        if random.random() < CROSSOVER_RATE:
            #parentA, parentB = tournamentSelection2(population[:size], tournamentSize)
            parentA = rankingSelection(population)
            parentB = rankingSelection(population)
            child = crossover_twopoint(parentA, parentB)
            new_population.append(child)
        else:
            #If crossover doesn't happen mutate random in top x%
            parentA = random.choice(population[:size])
            new_population.append(copy.deepcopy(mutate(parentA)))
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

def solve(n_size):
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
        population = tournamentPicking(population)    
        if generation + 1 == maximum_generation:
            return count_conflicts(best)
        
def experiment(n_size, repetitions):
    for i in range(repetitions):
        results = solve(n_size)

if __name__ == "__main__":
    population_size = 100
    for i in range(8):
        print(population_size)
        for i in range(10):
            print(solve(80))
        population_size += 50
