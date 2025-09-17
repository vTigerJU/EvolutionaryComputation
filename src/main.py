from chess import Board
# from test_collision import test_collision_detection

BOARD_SIZE = 4

if __name__ == "__main__":
    board = Board(BOARD_SIZE)
    print("8x8 Chess Board:")
    board.print_board_only()
    
    # Test fitness score
    fitness = board.fitness()
    print(f"Fitness score: {fitness}")

    # test_collision_detection()
