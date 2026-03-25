import time
import threading
from bfs import bfs
from astar import astar
from greedy import greedy

TIMEOUT_SECONDS = 10


def solve(board, algorithm):
    result_container = {}
    start_time = time.time()

    def run():
        if algorithm == "bfs":
            path, nodes = bfs(board)
        elif algorithm == "astar":
            path, nodes = astar(board)
        elif algorithm == "greedy":
            path, nodes = greedy(board)
        else:
            result_container["error"] = "Unknown algorithm"
            return
        result_container["path"] = path
        result_container["nodes"] = nodes

    thread = threading.Thread(target=run)
    thread.start()
    thread.join(timeout=TIMEOUT_SECONDS)

    end_time = time.time()

    if thread.is_alive():
        return {
            "error": f"Solver timed out after {TIMEOUT_SECONDS} seconds. Try a different algorithm."
        }

    if "error" in result_container:
        return {"error": result_container["error"]}

    path = result_container.get("path")
    nodes = result_container.get("nodes", 0)

    if path is None:
        return {"error": "Puzzle is unsolvable"}

    return {
        "path": path,
        "nodes_explored": nodes,
        "solution_length": len(path),
        "time_taken": round(end_time - start_time, 4)
    }


if __name__ == "__main__":
    board = [1, 2, 3, 0, 4, 6, 7, 5, 8]
    result = solve(board, "astar")
    print(result)
