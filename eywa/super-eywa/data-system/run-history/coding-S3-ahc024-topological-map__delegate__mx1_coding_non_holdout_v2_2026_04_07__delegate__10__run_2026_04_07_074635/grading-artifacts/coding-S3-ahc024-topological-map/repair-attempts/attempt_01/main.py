import sys

def solve():
    # Read N, M
    try:
        line1 = sys.stdin.readline().split()
        if not line1:
            return
        N = int(line1[0])
        M = int(line1[1])
    except EOFError:
        return

    # Read the grid
    grid = []
    for _ in range(N):
        grid.append(list(map(int, sys.stdin.readline().split())))

    # Build adjacency graph for colors 1..M
    adj = [set() for _ in range(M + 1)]
    for r in range(N):
        for c in range(N):
            color = grid[r][c]
            if color == 0:
                continue
            # Check neighbors
            for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < N and 0 <= nc < N:
                    n_color = grid[nr][nc]
                    if n_color != 0 and n_color != color:
                        adj[color].add(n_color)

    # We need to place colors 1..M on a 50x50 grid such that:
    # 1. Each color is connected (single cell is easiest).
    # 2. Adjacency is preserved (if adj[u] contains v, u and v must be adjacent).
    # 3. No new adjacencies are created.
    
    # This is a graph embedding problem. Since we want to maximize 0s,
    # we want to place colors in a way that uses minimal cells.
    # A simple approach: Greedy placement using a BFS/DFS order to keep neighbors close.
    
    output_grid = [[0 for _ in range(N)] for _ in range(N)]
    placed = [False] * (M + 1)
    
    # Start with color 1 (or the first available color)
    start_color = 1
    for i in range(1, M + 1):
        if any(grid[r][c] == i for r in range(N) for c in range(N)):
            start_color = i
            break
            
    # Use a simple spiral or snake-like placement to try and satisfy adjacencies
    # However, a simple greedy approach:
    # Place colors in a sequence. For each color, find a spot adjacent to an already placed neighbor.
    
    # To ensure we don't create illegal adjacencies, we must be careful.
    # But the problem says "Two colors must be adjacent in the output if and only if they were adjacent in the input."
    # This is a very strict condition (it's an induced subgraph embedding).
    
    # Let's try a very simple layout: place colors in a line if possible, 
    # but that only works for path graphs.
    # Given the constraints and the nature of the problem, a simple heuristic:
    # Place colors 1..M in a way that respects the graph.
    
    # Since we need a valid solution and the simplest one:
    # Let's try to place colors in a 1D-like structure or a small block.
    # If the graph is a simple path, we can place them in a line.
    # If it's more complex, we need a 2D layout.
    
    # Let's use a simple greedy placement:
    # 1. Pick an unplaced color.
    # 2. Try to place it in an empty cell that is adjacent to its already-placed neighbors.
    # 3. Check if this placement creates any illegal adjacencies with other placed colors.
    
    placed_coords = {} # color -> (r, c)
    
    def is_safe(color, r, c):
        # Check if placing 'color' at (r, c) creates illegal adjacencies
        for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < N and 0 <= nc < N:
                neighbor_color = output_grid[nr][nc]
                if neighbor_color != 0:
                    # If neighbor is already placed, check if they are supposed to be adjacent
                    if neighbor_color not in adj[color]:
                        return False
        # Also check if all required neighbors are already placed? 
        # No, because we can place them later. 
        # But we must ensure that when we place a neighbor, it's adjacent to this one.
        return True

    # Find a starting color
    current = start_color
    r, c = 25, 25 # Start in the middle
    output_grid[r][c] = current
    placed[current] = True
    placed_coords[current] = (r, c)
    
    # Queue for BFS-like placement
    queue = [current]
    visited_count = 1
    
    # We'll use a simple greedy approach: 
    # Try to place all colors.
    unplaced = [i for i in range(1, M + 1) if not placed[i]]
    
    # To make it more robust, we'll iterate through unplaced colors
    # and try to find a spot for them.
    for _ in range(M):
        found = False
        # Try to find a color that is adjacent to a placed color
        for color in unplaced:
            # Check if this color has any neighbors already placed
            neighbors_placed = []
            for neighbor in adj[color]:
                if placed[neighbor]:
                    neighbors_placed.append(placed_coords[neighbor])
            
            if neighbors_placed:
                # Try to find a cell adjacent to all neighbors_placed
                # and satisfies is_safe
                for nr, nc in neighbors_placed:
                    for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                        tr, tc = nr + dr, nc + dc
                        if 0 <= tr < N and 0 <= tc < N and output_grid[tr][tc] == 0:
                            if is_safe(color, tr, tc):
                                # Check if it's adjacent to ALL required neighbors that are already placed
                                # Actually, the rule is: "Two colors must be adjacent in the output 
                                # if and only if they were adjacent in the input."
                                # So if we place 'color' at (tr, tc), it MUST be adjacent to 
                                # all neighbors in adj[color] that are already placed.
                                
                                # Check adjacency to all placed neighbors
                                all_adj = True
                                for p_color in range(1, M + 1):
                                    if placed[p_color] and p_color in adj[color]:
                                        pr, pc = placed_coords[p_color]
                                        if abs(pr - tr) + abs(pc - tc) != 1:
                                            all_adj = False
                                            break
                                
                                if all_adj:
                                    output_grid[tr][tc] = color
                                    placed[color] = True
                                    placed_coords[color] = (tr, tc)
                                    unplaced.remove(color)
                                    found = True
                                    break
                    if found: break
            if found: break
        
        if not found:
            # If we can't find a spot for any unplaced color adjacent to placed ones,
            # just pick the first unplaced color and place it somewhere.
            if unplaced:
                color = unplaced[0]
                # Find an empty spot
                for tr in range(N):
                    for tc in range(N):
                        if output_grid[tr][tc] == 0:
                            if is_safe(color, tr, tc):
                                output_grid[tr][tc] = color
                                placed[color] = True
                                placed_coords[color] = (tr, tc)
                                unplaced.remove(color)
                                found = True
                                break
                    if found: break
            if not found:
                break

    # Print the grid
    for row in output_grid:
        print(*(row))

if __name__ == "__main__":
    solve()
