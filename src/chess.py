import random


class Board:
    board: list[int]

    def __init__(self, size: int | list[int]) -> None:
        if type(size) is list:
            self.board = size

        if type(size) is int:
            board = [rank_num for rank_num in range(1, size + 1)]
            random.shuffle(board)
            self.board = board

    def clone(self) -> "Board":
        return Board(self.board[:])

    def check_collision(self, i, n):
        for j in range(i + 1, n):
            piece_row = i + 1
            piece_col = self.board[i]

            target_row = j + 1
            target_col = self.board[j]

            # Check Vertical and Horizantal collision
            if piece_row == target_row or piece_col == target_col:
                return True

            # Check diagonal collision
            row_diff: int = abs(target_row - piece_row)
            col_diff: int = abs(target_col - piece_col)

            if row_diff == col_diff:
                return True
        return False

    def check_collisions(self):
        n = len(self.board)
        nbrOfCollisions = 0
        for i in range(n):
            if self.check_collision(i, n):
                nbrOfCollisions += 1
        return nbrOfCollisions

    def evaluate(self):
        collisions = self.check_collisions()
        if collisions > 0:
            print(f"Collision detected! {collisions} collisions.")
        else:
            print("No collisions.")
        return collisions

    def fitness(self):
        return self.check_collisions()

    def get_conflicted_queens(self):
        # Find which queens are involved in diagonal conflicts
        # and store them in a list.
        conflicted_queens = []

        for i, piece in enumerate(self.board):
            if self.check_collision(i, len(self.board)):
                conflicted_queens.append(f"({i + 1} {piece})")

        return conflicted_queens

    def print_board_only(self):
        print()
        for rank_idx, row in reversed(list(enumerate(self.board))):
            remain = len(self.board) - row
            empty = "( )"
            print(f"{rank_idx + 1} | {empty * (row - 1)}{str(row)}{empty * remain}")
        print()

    def print_positions(self, positions: list[int]):
        print(" ".join(str(position) for position in positions))
