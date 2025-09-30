import time
from chess import Board
import random
import numpy as np

# https://www.tutorialspoint.com/genetic_algorithms/genetic_algorithms_mutation.htm


class Mutation_Strategy:
    def __init__(
        self, strategies: list["Mutation_Strategy"] = [], verbose: bool = False
    ) -> None:
        self.strategies = strategies
        self.verbose = verbose

    def execute(self, population: list[Board]):
        self.mutate(population)
        for strategy in self.strategies:
            start = time.time()

            strategy.mutate(population)
            self.sort(population)  # sort between strategy

            elapsed = time.time() - start

            if self.verbose:
                # Calculate each strategy time: debugging purpose.
                print(f"{strategy.__class__.__name__}: {elapsed * 1000:.2f}ms")

    def mutate(self, population: list[Board]):
        pass

    def sort(self, population: list[Board]) -> None:
        fitness_scores = np.array([board.fitness() for board in population])

        top_indices = np.argsort(fitness_scores)[:]
        population[:] = [population[i].clone() for i in top_indices]

    def percent_of(self, any_number: int, percent: float) -> int:
        clamped_percent = max(0, min(percent, 100))
        return int(any_number * (clamped_percent / 100))


class Strategy_Swap_Mutation(Mutation_Strategy):
    """Mutation by switching two columns/row"""

    def __init__(
        self,
        mutation_rate: float = 0.1,
        elite_size_percent: int = 10,
    ) -> None:
        super().__init__()
        self.mutation_rate = mutation_rate
        self.elite_size_percent = elite_size_percent

    def mutate(self, population: list[Board]):
        # numpy random generates between 0-1.
        size = self.percent_of(len(population), self.elite_size_percent)  # keep top n%
        batch_generation = np.random.random(len(population)) < self.mutation_rate

        for board, should_mutate in zip(population, batch_generation):
            # Exclude the top elites.
            if size > 0:
                size = size - 1
                continue
            if should_mutate:
                self._mutate_(board.board)

    def _mutate_(self, position: list[int]):
        i, j = np.random.choice(len(position), 2, replace=False)
        position[i], position[j] = position[j], position[i]


class Strategy_Crossover(Mutation_Strategy):
    """Crossover operation - swap two node segment at random index"""

    def __init__(
        self,
        crossover_probability: float = 0.8,
        elite_size_percent: int = 10,
        tournament_size: int = 20,
    ) -> None:
        super().__init__()
        self.mutation_rate = crossover_probability
        self.elite_size_percent = elite_size_percent
        self.tournament_size = tournament_size

    def mutate(self, population: list[Board]):
        size = self.percent_of(len(population), self.elite_size_percent)  # keep top n%

        # pre calculate fitness scores. for faster lookup/find
        fitness_scores = np.array([board.fitness() for board in population])

        top_indices = np.argsort(fitness_scores)[:size]
        new_population = [population[i].clone() for i in top_indices]

        while len(new_population) < len(population):
            # Exclude the top elites.
            choice_range = range(size, len(population))

            if random.random() < self.mutation_rate:
                # Sample few random and pick the best.

                # Tournament A
                node_range_a = np.random.choice(
                    choice_range, self.tournament_size, replace=False
                )
                nodeA = node_range_a[np.argmin(fitness_scores[node_range_a])]
                node_a = population[nodeA]

                # Tournament B
                node_range_b = np.random.choice(
                    choice_range, self.tournament_size, replace=False
                )
                nodeB = node_range_b[np.argmin(fitness_scores[node_range_b])]
                node_b = population[nodeB]

                new_population.extend(self.crossover(node_a, node_b))
            else:
                nodes = np.random.choice(
                    choice_range, self.tournament_size, replace=False
                )
                node_best = population[np.argmin(fitness_scores[nodes])]
                new_population.append(node_best)

        population[:] = new_population[: len(population)]

    def crossover(self, nodeA: Board, nodeB: Board):
        copy_a = nodeA.clone()
        copy_b = nodeB.clone()

        start, end = np.sort(np.random.choice(len(copy_a.board), 2, replace=False))

        nodeA_slice = copy_a.board[start:end]
        nodeB_slice = copy_b.board[start:end]
        copy_a.board[start:end] = nodeB_slice
        copy_b.board[start:end] = nodeA_slice

        return (copy_a, copy_b)


class Strategy_Scramble_Mutation(Mutation_Strategy):
    """Scramble mutation - shuffle a random segment"""

    def __init__(
        self,
        mutation_rate: float = 0.05,
        elite_size_percent: int = 10,
    ) -> None:
        super().__init__()
        self.mutation_rate = mutation_rate
        self.elite_size_percent = elite_size_percent

    def mutate(self, population: list[Board]):
        size = self.percent_of(len(population), self.elite_size_percent)  # keep top n%
        batch_generation = np.random.random(len(population)) < self.mutation_rate

        for board, should_mutate in zip(population, batch_generation):
            # Exclude the top elites.
            if size > 0:
                size = size - 1
            if should_mutate:
                start, end = np.sort(
                    np.random.choice(len(board.board), 2, replace=False)
                )
                segment = board.board[start:end].copy()
                np.random.shuffle(segment)
                board.board[start:end] = segment


class Strategy_Inversion_Mutation(Mutation_Strategy):
    """Inversion mutation - reverse a random segment"""

    def __init__(
        self,
        mutation_rate: float = 0.05,
        elite_size_percent: int = 10,
    ) -> None:
        super().__init__()
        self.mutation_rate = mutation_rate
        self.elite_size_percent = elite_size_percent

    def mutate(self, population: list[Board]):
        size = self.percent_of(len(population), self.elite_size_percent)  # keep top n%
        batch_generation = np.random.random(len(population)) < self.mutation_rate

        for board, should_mutate in zip(population, batch_generation):
            # Exclude the top elites.
            if size > 0:
                size = size - 1
            if should_mutate:
                start, end = np.sort(
                    np.random.choice(len(board.board), 2, replace=False)
                )

                board.board[start:end] = list(reversed(board.board[start:end]))
