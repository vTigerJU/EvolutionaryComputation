import string


class Position:
    rank: str
    rank_num: int

    def __init__(self, rank, rank_num) -> None:
        self.rank = rank
        self.rank_num = rank_num

    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        return f"({self.rank},{self.rank_num})"

    def __eq__(self, value: object) -> bool:
        """Overrides the default implementation"""
        if isinstance(value, Position):
            is_rank_num = self.rank_num == value.rank_num
            is_rank = self.rank == value.rank
            return is_rank_num and is_rank
        return False


class Piece:
    name: str
    position: Position

    def __init__(self, name: str, position: Position) -> None:
        self.name = name
        self.position = position


class Board:
    # board_size: int
    # board: list[list[Position]] = []

    def __init__(self, size: int) -> None:
        self.board_size = size

        list_of_chars = list(string.ascii_lowercase)[:size]
        board: list[list[Position]] = []

        for rank_num in range(1, size + 1):
            board.append([Position(char, rank_num) for char in list_of_chars])

        self.board = board

    def print_board_only(self):
        print()
        for rank_idx, row in reversed(list(enumerate(self.board))):
            print(f"{rank_idx + 1} | " + "  ".join(str(pos) for pos in row))
        print()

    def print_positions(self, positions: list[Position]):
        print("  ".join(str(position) for position in positions))

    def get_column(self, position: Position):
        column = []
        index: int = -1

        for row in self.board:
            for i, pos in enumerate(row):
                if pos == position:
                    index = i

        if index == -1:
            return []

        for row in self.board:
            if position != row[index]:
                column.append(row[index])

        return column

    def get_rank_row(self, position: Position):
        clone = self.board[position.rank_num - 1].copy()
        clone.remove(position)
        return clone

    def get_position(self, rank: str, rank_num: int) -> Position:
        """Get a specific position on the board"""
        try:
            rank_index = ord(rank.lower()) - ord("a")
            return self.board[rank_num - 1][rank_index]
        except (IndexError, ValueError):
            raise ValueError(f"Invalid position: ({rank}, {rank_num})")


class Queen(Piece):
    def __init__(self, position: Position) -> None:
        super().__init__("Queen", position)

    def place(self, position: Position):
        self.position = position

    def move_spaces(self, board: Board):
        rank_row = board.get_rank_row(self.position)
        rank_column = board.get_column(self.position)

        board.print_positions(rank_row)
        board.print_positions(rank_column)

        # Need to implement diagonal
