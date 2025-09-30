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
BOARD_SIZE = 50
POPULATION_SIZE = 500
MAXIMUM_GENERATION = 300
ELITE_SIZE_PERCENT = 15
TOURNAMENT_SIZE = 30
RERUN_AMOUNT = 1

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
        # print(n_th_board.board, n_th_board.fitness())
        print("Current:", best.fitness(), "-", best.board)
        mutation_strategy.execute(population)

        # No solution found.
        if generation + 1 == MAXIMUM_GENERATION:
            return best.fitness()


if __name__ == "__main__":
    mutation_strats = Mutation_Strategy(
        [
            Strategy_Crossover(
                crossover_probability=CROSSOVER_PROBABILITY,
                elite_size_percent=ELITE_SIZE_PERCENT,
                tournament_size=TOURNAMENT_SIZE,
            ),
            Strategy_Swap_Mutation(
                mutation_rate=SWAP_RATE, elite_size_percent=ELITE_SIZE_PERCENT
            ),
            Strategy_Scramble_Mutation(
                mutation_rate=SCRAMBLE_RATE, elite_size_percent=ELITE_SIZE_PERCENT
            ),
            Strategy_Inversion_Mutation(
                mutation_rate=INVERSION_RATE, elite_size_percent=ELITE_SIZE_PERCENT
            ),
        ],
        verbose=False,
    )
    for i in range(RERUN_AMOUNT):
        print(solve(BOARD_SIZE, mutation_strats))
