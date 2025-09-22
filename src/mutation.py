from chess import Board, Piece
import random
import copy

# https://www.tutorialspoint.com/genetic_algorithms/genetic_algorithms_mutation.htm


class Mutation_Strategy:
    def __init__(self, strategies: list["Mutation_Strategy"] = []) -> None:
        self.strategies = strategies

    def execute(self, population: list[Board]):
        self.mutate(population)

        for strategy in self.strategies:
            strategy.execute(population)

    def mutate(self, population: list[Board]):
        pass


class Strategy_Swap_Mutation(Mutation_Strategy):
    """Mutation by switching two columns/row"""

    def __init__(self, mutation_rate: float = 0.1) -> None:
        super().__init__()
        self.mutation_rate = mutation_rate

    def mutate(self, population: list[Board]):
        for board in population:
            if random.random() < self.mutation_rate:
                self._mutate_(board.board)

    def _mutate_(self, position: list[Piece]):
        i, j = random.sample(range(len(position)), 2)
        position[i], position[j] = position[j], position[i]


class Strategy_Crossover(Mutation_Strategy):
    """Crossover operation - swap two node segment at random index"""

    def __init__(self, mutation_rate: float = 0.8) -> None:
        super().__init__()
        self.mutation_rate = mutation_rate

    def mutate(self, population: list[Board]):
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


class Strategy_Scramble_Mutation(Mutation_Strategy):
    """Scramble mutation - shuffle a random segment"""

    def __init__(self, mutation_rate=0.05) -> None:
        super().__init__()
        self.mutation_rate = mutation_rate

    def mutate(self, population: list[Board]):
        for board in population:
            if random.random() < self.mutation_rate:
                size = len(board.board)
                start, end = sorted(random.sample(range(size), 2))
                segment = board.board[start:end]
                random.shuffle(segment)
                board.board[start:end] = segment


class Strategy_Inversion_Mutation(Mutation_Strategy):
    """Inversion mutation - reverse a random segment"""

    def __init__(self, mutation_rate=0.05) -> None:
        super().__init__()
        self.mutation_rate = mutation_rate

    def mutate(self, population: list[Board]):
        for board in population:
            if random.random() < self.mutation_rate:
                size = len(board.board)
                start, end = sorted(random.sample(range(size), 2))
                board.board[start:end] = reversed(board.board[start:end])
