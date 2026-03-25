# 🧩 8-Puzzle Solver

An interactive web application that solves the classic **8-puzzle problem** using three AI search algorithms, visualised step-by-step in the browser. Built as a course project for an **Artificial Intelligence** class.

---

## 📖 What is the 8-Puzzle?

The 8-puzzle is a sliding tile puzzle on a 3×3 grid containing tiles numbered 1–8 and one blank space. The goal is to reach the following configuration by sliding tiles into the blank:

```
1  2  3
4  5  6
7  8  [ ]
```

It is a classic benchmark problem in AI used to study and compare **uninformed** vs **informed** search strategies.

---

## ✨ Features

- **Three search algorithms** with live performance comparison
- **Animated solution playback** to watch the puzzle solve itself step by step
- **Step counter** that shows current move progress (e.g. "Move 3 of 22") during animation
- **Image tile mode** can replace numbered tiles with a photo split across the grid
- **Show numbers toggle** to overlay tile numbers on image tiles or hide them
- **Speed slider** for control animation delay from 50ms (fast) to 1000ms (slow)
- **Shuffle / Reset** to randomise the board or return to the solved state
- **Stats panel** which includes nodes explored, solution length, and time taken per solve
- **Button locking** to disable shuffle/solve/reset  automatically during animation

---

## 🤖 Algorithms

All three algorithms share the same `PuzzleState` representation and **Manhattan distance** heuristic.

### Breadth-First Search (BFS)
An **uninformed** search that explores all states level by level. It always finds the **optimal (shortest) solution**, but explores a large number of nodes and uses significant memory — especially for harder boards.

### Greedy Best-First Search
An **informed** search that always expands the state closest to the goal according to the Manhattan distance heuristic (`h`). It is fast but **not guaranteed to find the optimal path** — it can take longer routes if they appear promising early on.

### A\* Search
An **informed** search combining the actual path cost from the start (`g`) and the heuristic estimate to the goal (`h`), so `f = g + h`. A\* is both **complete** and **optimal** — it finds the shortest solution while exploring far fewer nodes than BFS.

### Algorithm Comparison

| Algorithm | Optimal? | Complete? | Speed | Nodes Explored |
|-----------|----------|-----------|-------|----------------|
| BFS | ✅ Yes | ✅ Yes | Slow | High |
| Greedy | ❌ No | ✅ Yes | Fast | Low–Medium |
| A\* | ✅ Yes | ✅ Yes | Fast | Low |

---

## 🗂️ Project Structure

```
8-puzzle-solver/
│
├── app.py              # Flask web server — routes and API endpoint
├── solver.py           # Algorithm dispatcher with timeout protection
│
├── astar.py            # A* Search implementation
├── bfs.py              # Breadth-First Search implementation
├── greedy.py           # Greedy Best-First Search implementation
│
├── puzzle/
│   ├── __init__.py
│   └── state.py        # PuzzleState class — board logic, heuristics, neighbours
│
└── templates/
    └── index.html      # Full frontend — grid, controls, animation, image picker
```

---

## ⚙️ How It Works

### Backend

`PuzzleState` (`puzzle/state.py`) is the core data structure:

- The board is stored as a **tuple** for fast hashing and set membership checks
- **Manhattan distance** is computed with a precomputed goal-position lookup dict — O(1) per tile vs O(n) scan
- The heuristic result is **cached** on the state object so it is computed at most once per state
- `is_solvable()` checks the inversion count (O(n²)) and caches the result

When `/solve` is called via `POST`, `solver.py` dispatches to the chosen algorithm and wraps execution in a **10-second timeout thread** to prevent the server hanging on pathological inputs.

Each algorithm returns:
- `path` — list of board states from start to goal
- `nodes_explored` — total states dequeued/popped
- `solution_length` — number of moves
- `time_taken` — wall-clock seconds

### Frontend

The frontend (`templates/index.html`) communicates with Flask over `fetch`. On receiving a solution:

1. Stats (nodes, moves, time) are displayed immediately
2. The board animates through each step with a configurable delay
3. Buttons are disabled for the duration and re-enabled on completion

**Image tiles** work by setting `background-image` and `background-position` on each tile so that each tile shows the correct cropped slice of the photo. The slice is keyed to the tile's **goal position**, so when the puzzle is solved the full image appears seamlessly.

---

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- pip

### Installation

```bash
# Clone the repository
git clone https://github.com/your-username/8-puzzle-solver.git
cd 8-puzzle-solver

# Install dependencies
pip install flask
```

### Running

```bash
python app.py
```

Then open your browser at `http://127.0.0.1:5000`.

---

## 🛠️ Usage

1. Click **Shuffle** to randomise the board
2. Select an algorithm from the dropdown (A\*, BFS, or Greedy)
3. Adjust the **Speed** slider — drag right for faster, left for slower
4. Click **Solve** — the solution animates on the board and stats appear below
5. Optionally pick an **image preset** from the row of thumbnails to replace the coloured tiles with a photo
6. Toggle **Show numbers** to show/hide number overlays on image tiles
7. Click **Reset** to return to the solved state

---

## 📊 Example Results

For a moderately shuffled board (e.g. `[1, 2, 3, 0, 4, 6, 7, 5, 8]`):

| Algorithm | Nodes Explored | Moves | Time |
|-----------|---------------|-------|------|
| BFS | ~200–500 | Optimal | ~0.05s |
| Greedy | ~10–50 | Suboptimal | ~0.001s |
| A\* | ~20–80 | Optimal | ~0.003s |

Harder boards amplify the differences dramatically — BFS can explore tens of thousands of nodes while A\* solves the same board with a few hundred.

---

## 🧠 Key AI Concepts Demonstrated

- **State space search** — representing the puzzle as a graph of states
- **Heuristic functions** — Manhattan distance as an admissible, consistent heuristic
- **Admissibility** — Manhattan distance never overestimates, guaranteeing A\* optimality
- **Solvability checking** — using inversion count parity to reject unsolvable boards before searching
- **Performance trade-offs** — optimality vs speed vs memory across search strategies

---

## 🔧 Technical Notes

- BFS uses a `deque` for O(1) popleft; visited states are tracked by board tuple to avoid revisiting
- A\* uses a `heapq` min-heap; a tie-breaking counter ensures stable ordering for equal `f` values
- Greedy uses the same heap structure but ignores path cost `g`, using only `h`
- All `reconstruct_path` functions walk the parent chain and reverse it for correct ordering
- The solver runs in a daemon thread with a 10-second join timeout so Flask never hangs

---

## 📦 Dependencies

| Package | Purpose |
|---------|---------|
| `flask` | Web server and API routing |
| `heapq` | Priority queue for A\* and Greedy |
| `collections.deque` | BFS queue |
| `threading` | Solver timeout protection |

No external Python packages beyond Flask are required.

---

## 🎓 Course Context

This project was developed as part of an **Artificial Intelligence course** assignment. The objective was to make a small project using Artificial Intelligence. I built this using AI to implement and compare classical AI search algorithms on a well-known benchmark problem, and present the results through an interactive interface.
