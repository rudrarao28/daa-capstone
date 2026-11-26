import unittest
from src.city_graph import CityGraph
from src.algorithms import dijkstra, bellman_ford

class TestShortestPathAlgorithms(unittest.TestCase):
    def setUp(self):
        self.graph = CityGraph()
        self.graph.add_road("A", "B", 4)
        self.graph.add_road("A", "C", 2)
        self.graph.add_road("C", "B", 1)
        self.graph.add_road("B", "D", 5)
        self.graph.add_road("C", "D", 8)

    def test_dijkstra(self):
        distance, path = dijkstra(self.graph, "A", "D")
        self.assertEqual(distance, 8)
        self.assertEqual(path, ["A", "C", "B", "D"])

    def test_bellman_ford(self):
        distance, path = bellman_ford(self.graph, "A", "D")
        self.assertEqual(distance, 8)
        self.assertEqual(path, ["A", "C", "B", "D"])

    def test_unknown_location(self):
        with self.assertRaises(ValueError):
            dijkstra(self.graph, "X", "D")

if __name__ == "__main__":
    unittest.main()
