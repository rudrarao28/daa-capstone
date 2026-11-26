# Smart City Route Optimization System

A browser-based capstone project for finding efficient routes across a city network. It models locations as graph vertices and roads as weighted edges, then compares Dijkstra's and Bellman-Ford algorithms.

## Features
- Interactive web dashboard (no terminal menu).
- City locations and road connections overview.
- Shortest route calculation with Dijkstra or Bellman-Ford.
- Schematic road-network visualization with highlighted route.
- Benchmark comparison across graphs of 20, 50, 100 and 200 vertices.
- CSV benchmark export is available from the benchmark module.
- Unit tests.

## Requirements
- Python 3.9+
- Flask (installed using `requirements.txt`)

## Run in VS Code
1. Extract the ZIP and open the `Smart_City_Route_Optimization` folder in VS Code.
2. Open **Terminal → New Terminal**.
3. Install the dependency:
   ```bash
   python -m pip install -r requirements.txt
   ```
4. Start the dashboard:
   ```bash
   python app.py
   ```
5. Open your browser and visit **http://127.0.0.1:5000**.

Keep the terminal window open while using the dashboard. Press `Ctrl+C` in the terminal to stop the server.

## Test the algorithms
```bash
python -m unittest discover -s tests -v
```

## Algorithms
| Algorithm | Time complexity | Notes |
|---|---|---|
| Dijkstra (binary heap) | O((V + E) log V) | Efficient for non-negative road distances |
| Bellman-Ford | O(V × E) | Supports negative edges and detects negative cycles |

`V` is the number of vertices and `E` is the number of edges. Road distances in this project are non-negative, so Dijkstra is suitable.

## Customize the city network
Edit `data/city_roads.csv`. Keep the columns:
`source,destination,distance_km`

Each row represents a two-way road and its distance in kilometres.

## Project structure
```text
Smart_City_Route_Optimization/
├── app.py
├── main.py
├── requirements.txt
├── README.md
├── data/city_roads.csv
├── src/
│   ├── __init__.py
│   ├── algorithms.py
│   ├── benchmark.py
│   └── city_graph.py
├── templates/
│   └── index.html
├── static/
│   ├── app.js
│   └── style.css
└── tests/
    └── test_algorithms.py
```
