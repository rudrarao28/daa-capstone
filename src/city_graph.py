import csv
from collections import defaultdict

class CityGraph:
    """Weighted undirected graph: locations are vertices, roads are edges."""

    def __init__(self):
        self.adjacency = defaultdict(list)
        self.vertices = set()

    def add_road(self, source, destination, distance):
        if distance < 0:
            raise ValueError("Road distance cannot be negative.")
        self.vertices.update((source, destination))
        self.adjacency[source].append((destination, float(distance)))
        self.adjacency[destination].append((source, float(distance)))

    def add_vertex(self, location):
        self.vertices.add(location)
        self.adjacency[location]  # ensure the vertex has an adjacency list

    @classmethod
    def from_csv(cls, filepath):
        graph = cls()
        with open(filepath, newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                graph.add_road(row["source"].strip(),
                               row["destination"].strip(),
                               float(row["distance_km"]))
        return graph

    def validate_location(self, location):
        if location not in self.vertices:
            raise ValueError(f"Unknown location: {location}")
