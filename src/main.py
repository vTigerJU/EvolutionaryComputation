from chess import Board
# from test_collision import test_collision_detection

BOARD_SIZE = 5

if __name__ == "__main__":
    board = Board([2, 3, 4, 1])
    print("Chess Board:")
    board.print_board_only()

    # Test fitness score
    fitness = board.fitness()
    print(f"Fitness score: {fitness}")

    # Test conflicted queens
    print(f"Conflicted queens: {board.get_conflicted_queens()}")

    # test_collision_detection()
