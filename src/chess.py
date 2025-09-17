import random
from collisions import CollisionGroup

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
            
    def check_collision(self, i, n):
        for j in range(i + 1, n):
            piece_row = i + 1
            piece_col = self.board[i].position

            target_row = j + 1
            target_col = self.board[j].position

            # Check diagonal collision
            row_diff = abs(target_row - piece_row)
            col_diff = abs(target_col - piece_col)

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
    
    def find_collision_groups(self):
        n = len(self.board)
        slash_diagonals = {}
        backslash_diagonals = {}
        collision_groups = []
        
        for row_idx, piece in enumerate(self.board):
            row = row_idx + 1
            col = piece.position
            
            slash_id = row + col
            backslash_id = row - col
            
            if slash_id not in slash_diagonals:
                slash_diagonals[slash_id] = []
            slash_diagonals[slash_id].append((row, col))
            
            if backslash_id not in backslash_diagonals:
                backslash_diagonals[backslash_id] = []
            backslash_diagonals[backslash_id].append((row, col))
        
    def create_collisiongroup(self, i, n):
        for j in range(i + 1, n):
            piece_row = i + 1
            piece_col = self.board[i].position

            target_row = j + 1
            target_col = self.board[j].position

            # Check diagonal collision
            row_diff = abs(target_row - piece_row)
            col_diff = abs(target_col - piece_col)

            if row_diff == col_diff:
                return True
        return False
            
    def evaluate(self):
        if self.check_collisions():
            print("Collision detected!")
        else:   
            print("No collisions.")
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
