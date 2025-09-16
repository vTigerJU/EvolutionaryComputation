from chess import Board, Position, Queen

BOARD_SIZE = 8

if __name__ == "__main__":
    board = Board(8)
    print("8x8 Chess Board:")
    board.print_board_only()

    queen = Queen(Position(rank="b", rank_num=7))
    print(queen.move_spaces(board))
