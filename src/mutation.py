from chess import Piece
import random


class Mutation_Strategy:
    def __init__(self, strategies: list["Mutation_Strategy"]) -> None:
        self.strategies = strategies

    def execute(self, positions: list[Piece], population: list[list[Piece]]):
        self.mutate(positions, population)

        for strategy in self.strategies:
            strategy.execute(positions, population)

    def mutate(self, positions: list[Piece], population: list[list[Piece]]):
        pass


class Mutate_Strategy(Mutation_Strategy):
    def __init__(self, strategies: list["Mutation_Strategy"] = []) -> None:
        super().__init__(strategies)

    def mutate(self, positions: list[Piece], population: list[list[Piece]]):
        """Mutation by switching two columns"""
        i, j = random.sample(range(len(positions)), 2)
        positions[i], positions[j] = positions[j], positions[i]


class Crossover_Strategy(Mutation_Strategy):
    def __init__(self, strategies: list["Mutation_Strategy"] = []) -> None:
        super().__init__(strategies)

    def mutate(self, positions: list[Piece], population: list[list[Piece]]):
        """Swaps last half from each node"""
        new_pop = population[:10]
        for i in range(len(new_pop) // 2):
            self.crossover(new_pop[i], new_pop[i + 1])

        population[:10] = new_pop

    def crossover(self, nodeA: list[Piece], nodeB: list[Piece]):
        mid = len(nodeA) // 2
        nodeA_back = nodeA[mid:]
        nodeB_back = nodeB[mid:]
        nodeA[mid:] = nodeB_back
        nodeB[mid:] = nodeA_back
