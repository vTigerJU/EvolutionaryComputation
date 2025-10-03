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
from util import (
    Solve_Result,
    delete_write_file,
    log_board_info,
    run_taks_in_parallel,
    write_to_file,
)

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


def solve(n_size, mutation_strategy: Mutation_Strategy, thread_number: int = 1):
    start = time.time()
    population = [Board(n_size) for _ in range(POPULATION_SIZE)]

    for generation in range(MAXIMUM_GENERATION):
        population.sort(key=lambda x: x.fitness())
        best = population[0]

        if best.fitness() == 0:
            # Write the solution into file.
            # write_to_file(best)
            return Solve_Result(n_size, generation, start, best)

        # For displaying progress purpose. (kinda)
        log_board_info(best, start, thread_number)
        mutation_strategy.execute(population)

        # No solution found.
        if generation + 1 == MAXIMUM_GENERATION:
            # write_to_file(best)
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
    # Spawn thread for every rerun.
    results = run_taks_in_parallel(
        count=RERUN_AMOUNT,
        solve_task=solve,
        board_size=BOARD_SIZE,
        strategies=mutation_strats,
    )

    # delete the write file to remove old results.
    delete_write_file()
    for result in results:
        if result.is_found:
            # Only write the valid solutions to the file.
            write_to_file(result.solution)

    # Statistics and display in the terminal
    has_solutions = [result.is_found for result in results]
    solution_score = [result.solution.fitness() for result in results]
    avg_generation = [result.gen for result in results]
    avg_time = [result.time_s for result in results]

    # Fit everything in a 58 char length.
    print("\n┌" + "─" * 58 + "┐")
    print("│" + " GENETIC ALGORITHM RESULTS".center(58) + "│")
    print("├" + "─" * 58 + "┤")

    avg_rate = f"{round(average(has_solutions) * 100, 2)}%"
    avg_fitness = round(average(solution_score), 2)
    avg_gen = round(average(avg_generation), 2)
    avg_time = f"{round(average(avg_time), 2)}ms"
    print(f"│ {'Success rate ':.<20} │ {avg_rate:<33} │")
    print(f"│ {'Average fitness ':.<20} │ {avg_fitness:<33} │")
    print(f"│ {'Average generation ':.<20} │ {avg_gen:<33} │")
    print(f"│ {'Average time ':.<20} │ {avg_time:<33} │")

    print("├" + "─" * 58 + "┤")
    print("│" + " BEST SOLUTION".center(58) + "│")
    print("├" + "─" * 58 + "┤")

    # Extract the best run out of all reruns.
    results.sort(key=lambda x: x.solution.fitness())
    best = results[0]

    status = "SOLVED ✓" if best.is_found else "PARTIAL ✘"
    print(f"│ {'Status ':.<20} │ {status:<33} │")
    print(f"│ {'Best Fitness ':.<20} │ {best.solution.fitness():<33} │")
    print(f"│ {'Generation Found ':.<20} │ {best.gen:<33} │")
    print(f"│ {'Time Taken ':.<20} │ {best.time_s_str:<33} │")
    print("└" + "─" * 58 + "┘\n")
