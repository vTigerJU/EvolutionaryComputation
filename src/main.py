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
maximum_generation = 300
population_size = 200


def solve(n_size, mutation_strategy: Mutation_Strategy):
    start = time.time()

    population = [Board(n_size) for _ in range(population_size)]

    for generation in range(maximum_generation):
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
        if generation + 1 == maximum_generation:
            return best.fitness()


if __name__ == "__main__":
    mutation_strats = Mutation_Strategy(
        [
            Strategy_Crossover(mutation_rate=0.7),
            Strategy_Swap_Mutation(mutation_rate=0.1),
            Strategy_Scramble_Mutation(mutation_rate=0.05),
            Strategy_Inversion_Mutation(mutation_rate=0.05),
        ]
    )
    for i in range(10):
        print(solve(10, mutation_strats))
