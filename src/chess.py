import random


class Piece:
    position: int

    def __init__(self, rank) -> None:
        self.position = rank

    def place(self, position: int):
        self.position = position

    def __str__(self) -> str:
        return f"({self.position})"

    def __eq__(self, value: object) -> bool:
        """Overrides the default implementation"""
        if isinstance(value, Piece):
            return self.position == value.position
        return False


class Board:
    board: list[Piece]

    def __init__(self, size: int | list[int]) -> None:
        if type(size) is list:
            self.board = [Piece(piece) for piece in size]

        if type(size) is int:
            board = []
            for rank_num in range(1, size + 1):
                board.append(Piece(rank_num))

            random.shuffle(board)
            self.board = board

    def check_collision(self):
        n = len(self.board)
        for i in range(n):
            for j in range(i + 1, n):
                piece_row = i + 1
                piece_col = self.board[i].position

                target_row = j + 1
                target_col = self.board[j].position

                if piece_col == target_col:
                    return True

                # Check diagonal collision
                row_diff = abs(target_row - piece_row)
                col_diff = abs(target_col - piece_col)

                if row_diff == col_diff:
                    return True
        return False

    def evaluate(self):
        pass

    def print_board_only(self):
        print()
        for rank_idx, row in reversed(list(enumerate(self.board))):
            remain = len(self.board) - row.position
            empty = "( )"
            print(
                f"{rank_idx + 1} | {empty * (row.position - 1)}{str(row)}{empty * remain}"
            )
        print()

    def print_positions(self, positions: list[Piece]):
        print(" ".join(str(position) for position in positions))
