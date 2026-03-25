# Precomputed goal position lookup — eliminates O(n) scan per tile per state
GOAL_POSITIONS = {
    1: (0, 0), 2: (0, 1), 3: (0, 2),
    4: (1, 0), 5: (1, 1), 6: (1, 2),
    7: (2, 0), 8: (2, 1), 0: (2, 2)
}

GOAL_BOARD = (1, 2, 3, 4, 5, 6, 7, 8, 0)


class PuzzleState:
    def __init__(self, board, parent=None, move=None, depth=0):
        # Store as tuple from the start — no repeated list->tuple conversions
        self.board = tuple(board)
        self.parent = parent
        self.move = move
        self.depth = depth
        # Cache the heuristic so it's computed at most once per state
        self._manhattan = None
        # Cache solvability — it's an O(n²) check, only needed once
        self._solvable = None

    def get_blank_index(self):
        return self.board.index(0)

    def get_neighbors(self):
        neighbors = []
        blank = self.get_blank_index()
        row, col = divmod(blank, 3)

        moves = {
            "UP":    (row - 1, col),
            "DOWN":  (row + 1, col),
            "LEFT":  (row, col - 1),
            "RIGHT": (row, col + 1)
        }

        for move, (r, c) in moves.items():
            if 0 <= r < 3 and 0 <= c < 3:
                new_board = list(self.board)
                swap_index = r * 3 + c
                new_board[blank], new_board[swap_index] = new_board[swap_index], new_board[blank]
                neighbors.append(PuzzleState(new_board, parent=self, move=move, depth=self.depth + 1))

        return neighbors

    def manhattan_distance(self):
        # Return cached value if already computed
        if self._manhattan is not None:
            return self._manhattan

        distance = 0
        for i, tile in enumerate(self.board):
            if tile != 0:
                current_row, current_col = divmod(i, 3)
                goal_row, goal_col = GOAL_POSITIONS[tile]
                distance += abs(current_row - goal_row) + abs(current_col - goal_col)

        self._manhattan = distance
        return distance

    def is_goal(self):
        return self.board == GOAL_BOARD

    def is_solvable(self):
        if self._solvable is not None:
            return self._solvable

        tiles = [t for t in self.board if t != 0]
        inversions = 0
        for i in range(len(tiles)):
            for j in range(i + 1, len(tiles)):
                if tiles[i] > tiles[j]:
                    inversions += 1

        self._solvable = (inversions % 2 == 0)
        return self._solvable

    def __eq__(self, other):
        return self.board == other.board

    def __hash__(self):
        # board is already a tuple — no conversion needed
        return hash(self.board)
