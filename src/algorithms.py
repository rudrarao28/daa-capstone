import heapq
import math

def dijkstra(graph, start, destination):
    """Return (distance, path). Requires non-negative edge weights."""
    graph.validate_location(start)
    graph.validate_location(destination)

    distances = {vertex: math.inf for vertex in graph.vertices}
    previous = {}
    distances[start] = 0.0
    queue = [(0.0, start)]

    while queue:
        current_distance, current = heapq.heappop(queue)
        if current_distance != distances[current]:
            continue
        if current == destination:
            break
        for neighbour, weight in graph.adjacency[current]:
            new_distance = current_distance + weight
            if new_distance < distances[neighbour]:
                distances[neighbour] = new_distance
                previous[neighbour] = current
                heapq.heappush(queue, (new_distance, neighbour))

    if distances[destination] == math.inf:
        return None
    return distances[destination], _reconstruct_path(previous, start, destination)


def bellman_ford(graph, start, destination):
    """Return (distance, path); also detects reachable negative-weight cycles."""
    graph.validate_location(start)
    graph.validate_location(destination)
    edges = []
    for source in graph.vertices:
        for neighbour, weight in graph.adjacency[source]:
            edges.append((source, neighbour, weight))

    distances = {vertex: math.inf for vertex in graph.vertices}
    previous = {}
    distances[start] = 0.0

    for _ in range(len(graph.vertices) - 1):
        changed = False
        for source, destination_vertex, weight in edges:
            if distances[source] != math.inf and distances[source] + weight < distances[destination_vertex]:
                distances[destination_vertex] = distances[source] + weight
                previous[destination_vertex] = source
                changed = True
        if not changed:
            break

    for source, destination_vertex, weight in edges:
        if distances[source] != math.inf and distances[source] + weight < distances[destination_vertex]:
            raise ValueError("A reachable negative-weight cycle was detected.")

    if distances[destination] == math.inf:
        return None
    return distances[destination], _reconstruct_path(previous, start, destination)


def _reconstruct_path(previous, start, destination):
    path = [destination]
    while path[-1] != start:
        parent = previous.get(path[-1])
        if parent is None:
            return []
        path.append(parent)
    return list(reversed(path))
