import random
import time

maximum_generation = 200
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
    n = len(node) #Size of board
    count = 0   #Collision count
    for ix in range(n): # Check diagonal from left to right
        for j in range(ix+1,n):
            if abs(ix- j) == abs(node[ix] - node[j]): # if column diff == row diff
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

def solve(n_size, do_crossover):
    start = time.time()
    population = [random_solution(n_size) for _ in range(n_size)]

    for generation in range(maximum_generation):
        population.sort(key=count_conflicts)
        best = population[0]
        if count_conflicts(best) == 0:
            elapsed = time.time() - start
            return {
                "n": n_size,
                "gen": generation,
                "time_s": elapsed,
                #"solution": best,
                "found": True,
            }

        new_pop = population[:10]
        if(do_crossover):
            for i in range(len(new_pop)//2):
                new_pop[i], new_pop[i+1] = crossover(new_pop[i], new_pop[i+1])
        while len(new_pop) < population_size:
            parent = random.choice(population[:20])[:] 
            mutate(parent)
            new_pop.append(parent)
        population = new_pop

if __name__ == "__main__":
    
    for i in range(2):
        print(solve(100,True))
    
