from flask import Flask, jsonify, render_template, request
from src.city_graph import CityGraph
from src.algorithms import dijkstra, bellman_ford
from src.benchmark import run_benchmarks

app = Flask(__name__)
GRAPH = CityGraph.from_csv("data/city_roads.csv")

@app.get("/")
def home():
    return render_template("index.html")

@app.get("/api/locations")
def locations():
    roads = []
    seen = set()
    for source, neighbours in GRAPH.adjacency.items():
        for destination, distance in neighbours:
            key = tuple(sorted((source, destination)))
            if key not in seen:
                seen.add(key)
                roads.append({"source": source, "destination": destination, "distance": distance})
    return jsonify({"locations": sorted(GRAPH.vertices), "roads": roads})

@app.post("/api/route")
def route():
    data = request.get_json(silent=True) or {}
    start = data.get("start", "")
    end = data.get("end", "")
    algorithm = data.get("algorithm", "dijkstra")
    try:
        if algorithm == "bellman-ford":
            result = bellman_ford(GRAPH, start, end)
        elif algorithm == "dijkstra":
            result = dijkstra(GRAPH, start, end)
        else:
            return jsonify({"error": "Choose a valid algorithm."}), 400
        if result is None:
            return jsonify({"found": False, "message": "No route found."})
        distance, path = result
        return jsonify({"found": True, "distance": round(distance, 2), "path": path})
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400

@app.get("/api/benchmark")
def benchmark():
    rows = run_benchmarks()
    return jsonify(rows)

if __name__ == "__main__":
    print("Smart City dashboard: http://127.0.0.1:5000")
    app.run(debug=True)
