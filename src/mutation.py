from chess import Board, Piece
import random
import copy


class Mutation_Strategy:
    def __init__(self, strategies: list["Mutation_Strategy"]) -> None:
        self.strategies = strategies

    def execute(self, population: list[Board]):
        self.mutate(population)

        for strategy in self.strategies:
            strategy.execute(population)

    def mutate(self, population: list[Board]):
        pass


class Strategy_Mutate(Mutation_Strategy):
    def __init__(
        self, mutation_rate: float = 0.1, strategies: list[Mutation_Strategy] = []
    ) -> None:
        super().__init__(strategies)
        self.mutation_rate = mutation_rate

    def mutate(self, population: list[Board]):
        """Mutation by switching two columns"""

        for board in population:
            if random.random() < self.mutation_rate:
                self._mutate_(board.board)

    def _mutate_(self, position: list[Piece]):
        i, j = random.sample(range(len(position)), 2)
        position[i], position[j] = position[j], position[i]


class Strategy_Crossover(Mutation_Strategy):
    def __init__(
        self, mutation_rate: float = 0.8, strategies: list["Mutation_Strategy"] = []
    ) -> None:
        super().__init__(strategies)
        self.mutation_rate = mutation_rate

    def mutate(self, population: list[Board]):
        """Swaps last half from each node"""
        size = len(population) // 10  # keep top 10%
        new_population = population[:size]

        while len(new_population) < len(population):
            if random.random() < self.mutation_rate:
                # Sample few random and pick the best.
                nodeA = min(random.sample(population, size), key=lambda x: x.fitness())
                nodeB = min(random.sample(population, size), key=lambda x: x.fitness())
                # Pick only random.
                # nodeA = random.choice(population)
                # nodeB = random.choice(population)
                new_population.extend(list(self.crossover(nodeA, nodeB)))
            else:
                node = random.choice(population)
                new_population.append(copy.deepcopy(node))

        population[:] = new_population[: len(population)]

    def crossover(self, nodeA: Board, nodeB: Board):
        copy_a = copy.deepcopy(nodeA)
        copy_b = copy.deepcopy(nodeB)

        start, end = sorted(random.sample(range(len(copy_a.board)), 2))
        nodeA_slice = copy_a.board[start:end]
        nodeB_slice = copy_b.board[start:end]
        copy_a.board[start:end] = nodeB_slice
        copy_b.board[start:end] = nodeA_slice

        return (copy_a, copy_b)
