from flask import Flask, render_template, request, jsonify
from solver import solve

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/solve", methods=["POST"])
def solve_puzzle():
    data = request.get_json()
    board = data.get("board")
    algorithm = data.get("algorithm")

    if not board or len(board) != 9:
        return jsonify({"error": "Invalid board"}), 400

    result = solve(board, algorithm)
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)