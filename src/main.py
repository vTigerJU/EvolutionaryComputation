import time
from chess import Board
from mutation import (
    Strategy_Crossover,
    Strategy_Inversion_Mutation,
    Strategy_Swap_Mutation,
    Mutation_Strategy,
    Strategy_Scramble_Mutation,
)

# Setup
BOARD_SIZE = 20
POPULATION_SIZE = 2_000
MAXIMUM_GENERATION = 300
RERUN_AMOUNT = 10

# Probability
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

        # log n-th board.
        # n_th_board = population[len(population) - 10]
        # print(n_th_board, n_th_board.fitness())
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
    for i in range(RERUN_AMOUNT):
        print(solve(BOARD_SIZE, mutation_strats))
