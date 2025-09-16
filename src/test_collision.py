from chess import Board


def test_collision_detection():
    """Test the collision detection with known cases"""

    # Test cases
    test_cases = [
        ([2, 5, 3, 4, 6, 1, 7, 8], "Example"),
        ([6, 2, 7, 1, 4, 8, 5, 3], "Valid N-Queens solution"),
        ([1, 1, 1, 1, 1, 1, 1, 1], "All in same column - collision"),
        ([1, 2, 3, 4, 5, 6, 7, 8], "Main diagonal - collision"),
        ([8, 7, 6, 5, 4, 3, 2, 1], "Anti-diagonal - collision"),
        ([2, 4, 6, 8, 3, 1, 7, 5], "Another valid solution"),
    ]

    print("Testing collision detection:")
    print("=" * 50)

    for board_config, description in test_cases:
        board = Board(board_config)
        has_collision = board.check_collision()

        print(f"Board: {board_config}")
        print(f"Description: {description}")
        print(f"Has collision: {has_collision}")

        # Manual check for verification
        print("Manual verification:")
        positions = [(i + 1, board_config[i]) for i in range(len(board_config))]
        collisions = []

        for i, (r1, c1) in enumerate(positions):
            for j, (r2, c2) in enumerate(positions[i + 1 :], i + 1):
                if c1 == c2:
                    collisions.append(
                        f"Queens at ({r1},{c1}) and ({r2},{c2}) - same column"
                    )
                elif abs(r1 - r2) == abs(c1 - c2):
                    collisions.append(
                        f"Queens at ({r1},{c1}) and ({r2},{c2}) - diagonal"
                    )

        if collisions:
            for collision in collisions:
                print(f"  - {collision}")

            board.print_board_only()
        else:
            print("  - No collisions found")

        print("-" * 40)
