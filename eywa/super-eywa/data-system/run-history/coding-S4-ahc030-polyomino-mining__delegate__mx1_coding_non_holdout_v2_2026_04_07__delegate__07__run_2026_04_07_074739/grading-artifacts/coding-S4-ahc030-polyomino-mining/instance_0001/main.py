import sys
import math
import random

def solve():
    # Read initial input
    try:
        line = sys.stdin.readline()
        if not line:
            return
        parts = list(map(int, line.split()))
        if len(parts) < 4:
            return
        H, W, N_FIELDS, NOISE = parts[0], parts[1], parts[2], parts[3]
    except EOFError:
        return

    # Read polyomino shapes
    shapes = []
    for _ in range(N_FIELDS):
        line = sys.stdin.readline()
        if not line:
            break
        shape_parts = list(map(int, line.split()))
        # shape_parts[0] is number of cells, then x,y pairs
        cells = []
        for i in range(1, len(shape_parts), 2):
            cells.append((shape_parts[i], shape_parts[i+1]))
        shapes.append(cells)

    # State: Probability that cell (r, c) is oil
    # For simplicity in this baseline, we use a grid of probabilities
    prob_grid = [[0.0 for _ in range(W)] for _ in range(H)]
    # Initialize with a small prior
    for r in range(H):
        for c in range(W):
            prob_grid[r][c] = 0.01

    # Strategy: Bayesian Greedy Information Gain
    # We will probe cells that have high uncertainty or high potential
    # To keep it efficient, we'll use single-cell queries first
    
    queried = [[False for _ in range(W)] for _ in range(H)]
    
    # We'll limit the number of queries to stay within a reasonable cost budget
    # In a real competition, we'd use the noise parameter to decide between 'q 1' and 'q k'
    max_queries = (H * W) // 4
    queries_done = 0

    while queries_done < max_queries:
        # Find cell with highest uncertainty (0.5 is max uncertainty for Bernoulli)
        best_cell = None
        max_uncertainty = -1.0
        
        # Sample a subset of cells to speed up selection if grid is large
        search_space = []
        for r in range(H):
            for c in range(W):
                if not queried[r][c]:
                    search_space.append((r, c))
        
        if not search_space:
            break
            
        # Heuristic: pick a random unqueried cell or one with high prob
        # For a baseline, we'd implement more logic here