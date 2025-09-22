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
MAXIMUM_GENERATION = 300
POPULATION_SIZE = 200
CROSSOVER_PROBABILITY = 0.7
SWAP_RATE = 0.1
SCRAMBLE_RATE = 0.05
INVERSION_RATE = 0.05


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
                "time_s": "{:.2f}".format(elapsed),
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
    for i in range(10):
        print(solve(10, mutation_strats))
