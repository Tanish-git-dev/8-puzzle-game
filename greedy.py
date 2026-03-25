import heapq
from puzzle.state import PuzzleState


def greedy(start_board):
    start = PuzzleState(start_board)

    if not start.is_solvable():
        return None, 0

    if start.is_goal():
        return [], 0

    counter = 0
    heap = [(start.manhattan_distance(), counter, start)]
    visited = set()
    nodes_explored = 0

    while heap:
        h, _, current = heapq.heappop(heap)

        if current.board in visited:
            continue

        visited.add(current.board)
        nodes_explored += 1

        if current.is_goal():
            return reconstruct_path(current), nodes_explored

        for neighbor in current.get_neighbors():
            if neighbor.board not in visited:
                h = neighbor.manhattan_distance()  # cached after first call
                counter += 1
                heapq.heappush(heap, (h, counter, neighbor))

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
    path, nodes = greedy(board)
    end = time.time()

    print(f"Nodes explored: {nodes}")
    print(f"Solution length: {len(path)} moves")
    print(f"Time taken: {round(end - start, 4)} seconds")
    print("\nSolution steps:")
    for step in path:
        print(step)
