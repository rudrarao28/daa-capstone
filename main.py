from src.city_graph import CityGraph
from src.algorithms import dijkstra, bellman_ford
from src.benchmark import run_benchmarks, save_benchmark_csv

def show_locations(graph):
    print("\nAvailable locations:")
    for name in sorted(graph.vertices):
        print(f" - {name}")

def main():
    graph = CityGraph.from_csv("data/city_roads.csv")
    print("=" * 58)
    print("       SMART CITY ROUTE OPTIMIZATION SYSTEM")
    print("=" * 58)

    while True:
        print("\n1. View city locations and roads")
        print("2. Find shortest route (Dijkstra)")
        print("3. Find shortest route (Bellman-Ford)")
        print("4. Compare algorithm performance")
        print("5. Exit")
        choice = input("\nEnter choice: ").strip()

        if choice == "1":
            show_locations(graph)
            print("\nRoads (two-way):")
            for u in sorted(graph.adjacency):
                for v, w in graph.adjacency[u]:
                    if u < v:
                        print(f" {u} <--> {v}: {w} km")

        elif choice in ("2", "3"):
            show_locations(graph)
            start = input("\nStarting location: ").strip()
            end = input("Destination: ").strip()
            try:
                if choice == "2":
                    result = dijkstra(graph, start, end)
                    method = "Dijkstra"
                else:
                    result = bellman_ford(graph, start, end)
                    method = "Bellman-Ford"
                if result is None:
                    print("\nNo route exists between these locations.")
                else:
                    distance, path = result
                    print(f"\n{method} shortest route:")
                    print(" -> ".join(path))
                    print(f"Total distance: {distance:.2f} km")
            except ValueError as exc:
                print(f"\nError: {exc}")

        elif choice == "4":
            print("\nRunning benchmark on generated graphs...")
            rows = run_benchmarks()
            save_benchmark_csv(rows, "benchmark_results.csv")
            print(f"\n{'Vertices':>9} {'Edges':>9} {'Dijkstra (ms)':>16} {'Bellman-Ford (ms)':>20}")
            for row in rows:
                print(f"{row['vertices']:>9} {row['edges']:>9} "
                      f"{row['dijkstra_ms']:>16.3f} {row['bellman_ford_ms']:>20.3f}")
            print("\nDetailed results saved to benchmark_results.csv")

        elif choice == "5":
            print("\nThank you for using Smart City Route Optimization System!")
            break
        else:
            print("\nInvalid choice. Please enter 1 to 5.")

if __name__ == "__main__":
    main()
