import csv
import random
import time
from src.city_graph import CityGraph
from src.algorithms import dijkstra, bellman_ford

def generate_connected_graph(vertex_count, extra_edges_per_vertex=3, seed=42):
    """Create a connected, undirected graph with positive distances."""
    rng = random.Random(seed + vertex_count)
    graph = CityGraph()
    names = [f"Location_{i}" for i in range(vertex_count)]
    for name in names:
        graph.add_vertex(name)

    # A chain guarantees that every vertex is reachable.
    for i in range(vertex_count - 1):
        graph.add_road(names[i], names[i + 1], rng.randint(1, 30))

    # Add random roads to create a more realistic network.
    target_extra = vertex_count * extra_edges_per_vertex
    added = 0
    existing = {frozenset((names[i], names[i + 1])) for i in range(vertex_count - 1)}
    while added < target_extra:
        a, b = rng.sample(names, 2)
        key = frozenset((a, b))
        if key not in existing:
            graph.add_road(a, b, rng.randint(1, 30))
            existing.add(key)
            added += 1
    return graph

def _average_runtime(function, graph, start, end, repeats=3):
    timings = []
    for _ in range(repeats):
        begin = time.perf_counter()
        function(graph, start, end)
        timings.append((time.perf_counter() - begin) * 1000)
    return sum(timings) / len(timings)

def run_benchmarks(sizes=(20, 50, 100, 200), repeats=3):
    results = []
    for size in sizes:
        graph = generate_connected_graph(size)
        start, end = "Location_0", f"Location_{size - 1}"
        dijkstra_ms = _average_runtime(dijkstra, graph, start, end, repeats)
        bellman_ms = _average_runtime(bellman_ford, graph, start, end, repeats)
        edge_count = sum(len(v) for v in graph.adjacency.values()) // 2
        results.append({
            "vertices": size,
            "edges": edge_count,
            "dijkstra_ms": round(dijkstra_ms, 4),
            "bellman_ford_ms": round(bellman_ms, 4)
        })
    return results

def save_benchmark_csv(rows, filepath):
    with open(filepath, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=[
            "vertices", "edges", "dijkstra_ms", "bellman_ford_ms"
        ])
        writer.writeheader()
        writer.writerows(rows)
