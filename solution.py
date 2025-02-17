from collections import defaultdict, deque

class Solution:
    def get_k_popular_pins(self, pins: list[list[int]], k: int, depth: int) -> list[int]:
        # Create an adjacency list to represent the graph
        graph = defaultdict(list)
        for pin, related_pin in pins:
            graph[pin].append(related_pin)
        
        # Initialize a set to keep track of visited pins
        visited = set()
        
        # Initialize a list to store the result
        result = []
        
        # Define a helper function for DFS
        def dfs(pin, current_depth):
            # Mark the current pin as visited
            visited.add(pin)
            
            # Add the current pin to the result
            result.append(pin)
            
            # If the current depth is less than the given depth, continue exploring
            if current_depth < depth:
                for related_pin in graph[pin]:
                    if related_pin not in visited:
                        dfs(related_pin, current_depth + 1)
        
        # Perform DFS on each unvisited pin
        for pin, _ in pins:
            if pin not in visited:
                dfs(pin, 0)
        
        # Return the k most popular pins based on the given criteria
        return result[:k]


# Test the function
solution = Solution()
print(solution.get_k_popular_pins([
    [1123, 643],
    [1123, 221],
    [221, 563],
    [221, 1123],
    [643, 987],
    [563, 1123],
    [987, 563],
    [101, 321],
    [123, 0]
], 6, 2))  # Expected output: [1123, 643, 987, 221, 563, 101]

print(solution.get_k_popular_pins([
    [1123, 643],
    [1123, 221],
    [221, 563],
    [221, 1123],
    [643, 987],
    [563, 1123],
    [987, 563],
    [101, 321],
    [123, 0]
], 6, 1))  # Expected output: [1123, 643, 221, 563, 987, 101]

print(solution.get_k_popular_pins([
    [1123, 643],
    [1123, 221],
    [221, 563],
    [221, 1123],
    [643, 987],
    [563, 1123],
    [987, 563],
    [101, 321],
    [123, 0]
], 6, 0))  # Expected output: [1123, 221, 643, 563, 987, 101]
