from collections import deque
from puzzle.state import PuzzleState


def bfs(start_board):
    start = PuzzleState(start_board)

    if not start.is_solvable():
        return None, 0

    if start.is_goal():
        return [], 0

    queue = deque([start])
    # Track by board tuple directly — faster than hashing the full object
    visited = {start.board}
    nodes_explored = 0

    while queue:
        current = queue.popleft()
        nodes_explored += 1

        for neighbor in current.get_neighbors():
            if neighbor.board not in visited:
                # Goal check on dequeue (consistent with other algorithms)
                # and avoids adding the goal to the queue unnecessarily
                visited.add(neighbor.board)

                if neighbor.is_goal():
                    return reconstruct_path(neighbor), nodes_explored

                queue.append(neighbor)

    return None, nodes_explored


def reconstruct_path(state):
    path = []
    while state.parent is not None:
        path.append(list(state.board))
        state = state.parent
    path.reverse()
    return path


if __name__ == "__main__":
    import time

    board = [1, 2, 3, 0, 4, 6, 7, 5, 8]

    start = time.time()
    path, nodes = bfs(board)
    end = time.time()

    print(f"Nodes explored: {nodes}")
    print(f"Solution length: {len(path)} moves")
    print(f"Time taken: {round(end - start, 4)} seconds")
    print("\nSolution steps:")
    for step in path:
        print(step)
