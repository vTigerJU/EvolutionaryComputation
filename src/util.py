from concurrent.futures.process import ProcessPoolExecutor
from os import remove
import time

from chess import Board
from mutation import Mutation_Strategy


class Solve_Result:
    def __init__(
        self, n_size: int, generation: int, start_time: float, best: Board
    ) -> None:
        elapsed = time.time() - start_time
        self.n = n_size
        self.gen = generation
        self.time_s = elapsed
        self.time_s_str = "{:.2f}ms".format(elapsed)
        self.solution = best
        self.is_found = best.fitness() == 0


def write_to_file(board: Board) -> None:
    with open("./solution.txt", "a+") as f:
        print(board.board, file=f)


def delete_write_file() -> None:
    remove("./solution.txt")


def log_board_info(board: Board, start_time: float, thread_num: int = 1) -> None:
    # log n-th board.
    # n_th_board = population[len(population) - 10]
    # print(n_th_board.board, n_th_board.fitness())
    print(
        f"[ {thread_num:<2} ]",
        "Current score:",
        board.fitness(),
        "-",
        board.board,
        f"{(time.time() - start_time) * 1000:.1f}ms",
    )


def run_taks_in_parallel(
    count: int, solve_task, board_size: int, strategies: Mutation_Strategy
) -> list[Solve_Result]:
    with ProcessPoolExecutor() as executor:
        running_tasks = [
            executor.submit(solve_task, board_size, strategies, i + 1)
            for i in range(count)
        ]
        results = [task.result() for task in running_tasks]

    return results
