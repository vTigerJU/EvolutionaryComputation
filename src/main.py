import time
from numpy import average

from chess import Board
from mutation import (
    Strategy_Crossover,
    Strategy_Inversion_Mutation,
    Strategy_Swap_Mutation,
    Mutation_Strategy,
    Strategy_Scramble_Mutation,
)
from util import Solve_Result, run_taks_in_parallel, write_to_file

# Setup
BOARD_SIZE = 50
POPULATION_SIZE = 500
MAXIMUM_GENERATION = 300
ELITE_SIZE_PERCENT = 15
TOURNAMENT_SIZE = 30
RERUN_AMOUNT = 25

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
            # Write the solution into file.
            write_to_file(best)
            return Solve_Result(n_size, generation, start, best)

        # log_board_info(best, start)
        mutation_strategy.execute(population)

        # No solution found.
        if generation + 1 == MAXIMUM_GENERATION:
            write_to_file(best)
            return Solve_Result(n_size, generation, start, best)


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

if __name__ == "__main__":
    results = run_taks_in_parallel(
        count=RERUN_AMOUNT,
        solve_task=solve,
        board_size=BOARD_SIZE,
        strategies=mutation_strats,
    )
    for i in range(RERUN_AMOUNT):
        print(solve(BOARD_SIZE, mutation_strats))
