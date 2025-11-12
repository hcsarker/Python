import math
import heapq
import random
import numpy as np

class Node:
    def __init__(self, val, heuristics=0):
        self.val = val 
        self.neighbors = []
        self.heuristics = heuristics


# <----------------------take input:-------------------------------->
def take_input():
    nodes = {}
    print("Enter node and heuristics: (write 'done' after finished)")
    while True:
        data = input().split()
        
        if data[0] == "done":
            break
        if len(data) != 2:
            print("invalid input")
            continue
        
        val, huris = int(data[0]), int(data[1])
        nodes[val] = Node(val, huris)
        
    print("Enter node1, node2, cost (write 'done' when finished):")
    while True:
        data = input().split()
        if data[0] == "done":
            break
        if len(data) != 3:
            print("invalid value")
            continue
        
        u, v, w = int(data[0]), int(data[1]), int(data[2])
        if u not in nodes:
            nodes[u] = Node(u, 0)
        if v not in nodes:
            nodes[v] = Node(v, 0)
            
        nodes[u].neighbors.append((nodes[v], w))
        
    start = int(input("start node: "))
    target = int(input("target node: "))
    
    if start not in nodes or target not in nodes:
        print("start or target node is invalid")
        return None, None, None
    
    return nodes[start], nodes[target], nodes



#<-------------------------------Hill Climbing Search-------------------------------->
def hill_climbing(start, target):
    """
    Hill Climbing: Always moves to the best immediate neighbor
    """
    if not start or not target:
        return None
    
    current = start
    path = [current.val]
    visited = set([current.val])
    
    while current != target:
        # Find the best neighbor: (lowest heuristic, as i note)
        best_neighbor = None
        best_heuristic = float('inf')
        
        for neighbor, cost in current.neighbors:
            if neighbor.val not in visited and neighbor.heuristics < best_heuristic:
                best_heuristic = neighbor.heuristics
                best_neighbor = neighbor
        
        # If no better neighbor found, we're stuck
        if best_neighbor is None:
            print("Hill Climbing: Reached local optimum, cannot proceed to target")
            return None
        
        # Move to the best neighbor
        current = best_neighbor
        path.append(current.val)
        visited.add(current.val)
        
        # Safety check to avoid infinite loops
        if len(path) > 100: 
            print("Hill Climbing: Path too long, likely stuck in loop")
            return None
    return path



#<----------------------------------Beam Search------------------------------------>
def beam_search(start, target, beam_width=2):
    """
    Beam Search: Keeps only the top 'beam_width' most promising nodes at each level
    in memory.
    """
    if not start or not target:
        return None
    
    # Each element: (heuristic, node, path)
    current_level = [(start.heuristics, start, [start.val])]
    visited = set()
    while current_level:
        next_level = []
        # Expand all nodes in current level
        for heuristic, node, path in current_level:
            if node == target:
                return path
            if node in visited:
                continue
            visited.add(node)
            
            # Add all neighbors to next level
            for neighbor, cost in node.neighbors:
                if neighbor not in visited:
                    new_path = path + [neighbor.val]
                    next_level.append((neighbor.heuristics, neighbor, new_path))
        
        # If no more nodes to explore
        if not next_level:
            return None
        
        # Keep only the top beam_width nodes (based on heuristic)
        next_level.sort(key=lambda x: x[0])
        current_level = next_level[:beam_width]
        
        # Safety check for infinite loop
        if len(path) > 100:
            print("Beam Search: Path too long")
            return None
    return None

#<----------------------------------Simulated Annealing--------------------------------->
def simulated_annealing(start, target, initial_temp=1000, cooling_rate=0.95, max_iterations=1000):
    """
    Simulated Annealing: Sometimes accepts worse moves to escape local optima:
    
    - Similated annelaing is a metaheuristic algorithrm which is inspired from metal 
        annelaing.
        
    - Which can scape the local optima and reached into the global optima.
    
    - Intial temp: high -> High Randomnes.
    
    - Cooling rate (0.95): The temperature is multiplied by the cooling rate at each step,
      so it gradually decreases. As the temperature decreases, the algorithm becomes more 
      deterministic (like hill climbing) because the probability of accepting worse moves 
      decreases.
      
    """
    if not start or not target:
        return None
    
    current = start
    current_path = [current.val]
    current_heuristic = current.heuristics
    
    temperature = initial_temp
    
    for i in range(max_iterations):
        if current == target:
            return current_path
        
        # If no neighbors, we're stuck
        if not current.neighbors:
            return None
        
        # Randomly select a neighbor
        neighbor, cost = random.choice(current.neighbors)
        
        neighbor_heuristic = neighbor.heuristics
        
        # Calculate the change in heuristic (we want to minimize)
        delta_e = neighbor_heuristic - current_heuristic
        
        # If neighbor is better, always accept
        # If neighbor is worse, accept with probability based on temperature
        # P(accept worse move) = exp(-ΔE / T)
        if delta_e < 0 or random.random() < math.exp(-delta_e / (temperature + 1e-10)):
            current = neighbor
            current_path.append(current.val)
            current_heuristic = neighbor_heuristic
        
        # Cool down
        temperature *= cooling_rate
        
        # If temperature is very low, do hill climbing
        if temperature < 1e-10:
            # Fall back to hill climbing for the remaining steps
            temp_current = current
            temp_path = current_path.copy()
            
            while temp_current != target and len(temp_path) < len(current_path) + 50:
                best_neighbor = None
                best_heuristic = float('inf')
                
                for n, c in temp_current.neighbors:
                    if n.val not in temp_path and n.heuristics < best_heuristic:
                        best_heuristic = n.heuristics
                        best_neighbor = n
                
                if best_neighbor is None:
                    break
                
                temp_current = best_neighbor
                temp_path.append(temp_current.val)
            
            if temp_current == target:
                return temp_path
            break
    
    return None

# Unified Local Search Function
def local_search(start, target, algorithm="beam", **kwargs):
    """
    Unified local search function that can run different algorithms based on parameters
    """
    if algorithm == "hill_climbing":
        return hill_climbing(start, target)
    
    elif algorithm == "beam":
        beam_width = kwargs.get('beam_width', 2)
        return beam_search(start, target, beam_width)
    
    elif algorithm == "simulated_annealing":
        initial_temp = kwargs.get('initial_temp', 1000)
        cooling_rate = kwargs.get('cooling_rate', 0.95)
        max_iterations = kwargs.get('max_iterations', 1000)
        return simulated_annealing(start, target, initial_temp, cooling_rate, max_iterations)
    
    else:
        raise ValueError("Unknown algorithm")


""" 

"""

# Test all algorithms
if __name__ == "__main__":
    start_node, target_node, all_nodes = take_input()
    
    if start_node and target_node:
        print("\n" + "="*50)
        print("Testing Local Search Algorithms")
        print("="*50)
        
        # Test Hill Climbing
        print("\n1. Hill Climbing Search:")
        path = hill_climbing(start_node, target_node)
        if path:
            print(f"Path found: {path}")
        else:
            print("No path found")
        
        # Test Beam Search with different beam widths
        print("\n2. Beam Search:")
        for beam_width in [1, 2, 3]:
            path = beam_search(start_node, target_node, beam_width)
            if path:
                print(f"Beam width {beam_width}: Path found: {path}")
            else:
                print(f"Beam width {beam_width}: No path found")
        
        # Test Simulated Annealing
        print("\n3. Simulated Annealing:")
        path = simulated_annealing(start_node, target_node)
        if path:
            print(f"Path found: {path}")
        else:
            print("No path found")
        
        # Test unified function
        print("\n4. Unified Local Search Function:")
        algorithms = [
            ("hill_climbing", {}),
            ("beam", {"beam_width": 2}),
            ("simulated_annealing", {})
        ]
        
        for algo_name, params in algorithms:
            path = local_search(start_node, target_node, algorithm=algo_name, **params)
            if path:
                print(f"{algo_name}: Path found: {path}")
            else:
                print(f"{algo_name}: No path found")
                
        
    