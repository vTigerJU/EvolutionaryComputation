import time
from chess import Board
from mutation import (
    Strategy_Crossover,
    Strategy_Inversion_Mutation,
    Strategy_Swap_Mutation,
    Mutation_Strategy,
    Strategy_Scramble_Mutation,
)

BOARD_SIZE = 10
MAXIMUM_GENERATION = 150
POPULATION_SIZE = 200
CROSSOVER_PROBABILITY = 0.7
SWAP_RATE = 0.1
SCRAMBLE_RATE = 0.05
INVERSION_RATE = 0.05


def experiment():
    solution_attempts = 1
    board_size = 50
    #print("Crossover")
    #mutation_strats = Mutation_Strategy([Strategy_Crossover(crossover_probability=CROSSOVER_PROBABILITY)])
    #print(solve_multiple(board_size,mutation_strats, solution_attempts))
    print("Swap")
    mutation_strats = Mutation_Strategy([Strategy_Swap_Mutation(mutation_rate=SWAP_RATE)])
    print(solve_multiple(board_size,mutation_strats, solution_attempts))
    print("Scramble")
    mutation_strats = Mutation_Strategy([Strategy_Scramble_Mutation(mutation_rate=SCRAMBLE_RATE)])
    print(solve_multiple(board_size,mutation_strats, solution_attempts))
    print("Inversion")
    mutation_strats = Mutation_Strategy([Strategy_Inversion_Mutation(mutation_rate=INVERSION_RATE)])
    print(solve_multiple(board_size,mutation_strats, solution_attempts))
    
def solve_multiple(n_size, mutation_strategy: Mutation_Strategy, sample_size):
    avg_gen = 0
    avg_time_s = 0
    number_failures = 0
    for i in range(sample_size):
        solution = solve(n_size, mutation_strategy)
        try:
            avg_gen += solution.get("gen")
            avg_time_s += solution.get("time_s")
        except:
            number_failures +=1

    if sample_size != number_failures:
        avg_gen = avg_gen/(sample_size - number_failures)
        avg_time_s = avg_time_s/(sample_size - number_failures)
    return {
        "n": n_size,
        "avg_gen": avg_gen,
        "avg_time_s": avg_time_s,
        "failures": number_failures
    }

def solve(n_size, mutation_strategy: Mutation_Strategy):
    start = time.time()

    population = [Board(n_size) for _ in range(POPULATION_SIZE)]

    for generation in range(MAXIMUM_GENERATION):
        population.sort(key=lambda x: x.fitness())
        best = population[0]

        if best.fitness() == 0:
            elapsed = time.time() - start
            return {
                "n": n_size,
                "gen": generation,
                "time_s": elapsed,#"{:.2f}".format(elapsed)
                # "solution": str(best),
                "found": True,
            }

        mutation_strategy.execute(population)

        # No solution found.
        if generation + 1 == MAXIMUM_GENERATION:
            return best.fitness()


if __name__ == "__main__":
    mutation_strats = Mutation_Strategy(
        [
            Strategy_Crossover(crossover_probability=CROSSOVER_PROBABILITY),
            Strategy_Swap_Mutation(mutation_rate=SWAP_RATE),
            Strategy_Scramble_Mutation(mutation_rate=SCRAMBLE_RATE),
            Strategy_Inversion_Mutation(mutation_rate=INVERSION_RATE),
        ]
    )
    experiment()
