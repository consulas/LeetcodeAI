from collections import defaultdict

class Solution:
    def build_graph(pins):
        graph = defaultdict(list)
        for pin, related in pins:
            graph[pin].append(related)
        return graph

    def dfs(graph, current_pin, depth, k, visited):
        if depth <= 0 or len(visited) == k:
            return
    
        for point in graph.get(current_pin, []):
            if point not in visited:
                visited.append(point)
                dfs(graph, point, depth - 1, k, visited)

    def get_k_popular_pins(pins, k, depth):
        graph = build_graph(pins)
        visited = []
        index = 0
    
        while len(visited) < k and index < len(pins):
            pin = pins[index][0]
            if pin not in visited:
                visited.append(pin)
                dfs(graph, pin, depth, k, visited)
            index += 1
    
        return visited

# Sample Test Case
# pins = [
#     (1123, 643), (1123, 221), (221, 563), (221, 1123), (643, 987),
#     (563, 1123), (987, 563), (101, 321), (123, 0)
# ]

# print(get_k_popular_pins(pins, 6, 2))  # [1123, 643, 987, 221, 563, 101]
# print(get_k_popular_pins(pins, 6, 1))  # [1123, 643, 221, 563, 987, 101]
# print(get_k_popular_pins(pins, 6, 0))  # [1123, 221, 643, 563, 987, 101]