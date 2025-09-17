from chess import Board
# from test_collision import test_collision_detection

BOARD_SIZE = 8

if __name__ == "__main__":
    board = Board(4)
    print("8x8 Chess Board:")
    board.print_board_only()
    print(board.check_collisions())
    # test_collision_detection()
