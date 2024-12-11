from flask import Flask, render_template, request, jsonify
import heapq

app = Flask(__name__)

def a_star_algorithm(graph, start, goal):
    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}
    g_score = {node: float('inf') for node in graph}
    g_score[start] = 0
    f_score = {node: float('inf') for node in graph}
    f_score[start] = heuristic(start, goal)
    
    while open_set:
        _, current = heapq.heappop(open_set)
        
        if current == goal:
            return reconstruct_path(came_from, current)
        
        for neighbor, weight in graph[current].items():
            tentative_g_score = g_score[current] + weight
            if tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = g_score[neighbor] + heuristic(neighbor, goal)
                heapq.heappush(open_set, (f_score[neighbor], neighbor))
    
    return None

def heuristic(node, goal):
    return 0

def reconstruct_path(came_from, current):
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.append(current)
    path.reverse()
    return path

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/solve', methods=['POST'])
def solve():
    try:
        data = request.json
        cities = data.get('cities', [])
        distances = data.get('distances', [])
        start = data.get('start')
        goal = data.get('goal')

        if not cities or not distances or not start or not goal:
            return jsonify({'error': 'Invalid input data'}), 400

        graph = {city: {} for city in cities}

        for dist in distances:
            from_city = dist.get('from')
            to_city = dist.get('to')
            distance = dist.get('distance')

            if not from_city or not to_city or distance is None:
                return jsonify({'error': 'Invalid distance entry'}), 400

            if from_city not in graph:
                graph[from_city] = {}
            if to_city not in graph:
                graph[to_city] = {}

            graph[from_city][to_city] = distance
            graph[to_city][from_city] = distance

        print("Graph:", graph)  

        path = a_star_algorithm(graph, start, goal)

        return jsonify({'path': path})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 500
if __name__ == '__main__':
    app.run(debug=True)
