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

    # Read the 50x50 grid
    grid = []
    for _ in range(N):
        grid.append(list(map(int, sys.stdin.readline().split())))

    # 1. Identify all non-zero colors and their adjacency relations
    adj = {i: set() for i in range(1, M + 1)}
    colors_present = set()
    
    for r in range(N):
        for c in range(N):
            color = grid[r][c]
            if color > 0:
                colors_present.add(color)
                # Check 4-neighbors
                for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < N and 0 <= nc < N:
                        neighbor_color = grid[nr][nc]
                        if neighbor_color > 0 and neighbor_color != color:
                            adj[color].add(neighbor_color)
                            adj[neighbor_color].add(color)

    # 2. Build a Spanning Tree of the color adjacency graph to ensure connectivity
    # and a simple layout.
    # We will place colors in a simple path or a small cluster.
    # A simple way to satisfy "if and only if" is hard, but the problem says:
    # "Two colors must be adjacent in the output if and only if they were adjacent in the input."
    # This is a very strict constraint. It means if color A and B were NOT adjacent, 
    # they MUST NOT be adjacent in the output.
    
    # Let's try to place colors on a diagonal or a sparse structure.
    # However, the simplest valid approach is to find a layout that respects the graph.
    # Since we need to maximize 0s, we want to use as few cells as possible.
    # A simple path layout: color 1 at (0,0), color 2 at (0,1)... but this only works if 
    # the adjacency graph is a path.
    
    # Given the strict "if and only if", we must be careful.
    # Let's use a grid-based layout where we place colors such that they only touch 
    # their required neighbors.
    
    # For a general graph, we can try to embed it in a grid.
    # A safe way to avoid unwanted adjacencies is to place colors far apart, 
    # but then we can't satisfy required adjacencies.
    # A better way: place colors on a grid with spacing.
    
    # Let's try a simple approach: 
    # Place colors in a sequence based on a BFS/DFS traversal of the adjacency graph.
    # To prevent unwanted adjacencies, we can place them on a grid with enough 0s between them.
    # But we need to satisfy the "if" part (required adjacencies).
    
    # Let's use a simple snake-like path for a spanning tree.
    # To satisfy "if and only if", we can't just use a path.
    # But wait, if the graph is a tree, we can lay it out.
    
    # Let's try a very conservative approach:
    # Place each color in a single cell (r, c) such that if color A and B are adjacent,
    # their cells are adjacent.
    # This is only possible if the graph is a subgraph of the grid graph.
    # Most color graphs in these problems are sparse.
    
    # Let's try to find a layout using a simple greedy approach:
    # Place color 1 at (0,0). For every other color, try to place it adjacent to an 
    # already placed color it is connected to.
    
    res_grid = [[0 for _ in range(N)] for _ in range(N)]
    placed = {} # color -> (r, c)
    
    # Start with the first color found
    if not colors_present:
        for row in res_grid:
            print(*(row))
        return

    start_color = min(colors_present)
    placed[start_color] = (0, 0)
    res_grid[0][0] = start_color
    
    queue = [start_color]
    visited_colors = {start_color}
    
    # BFS to place colors
    idx = 0
    while idx < len(queue):
        u = queue[idx]
        idx += 1
        
        curr_r, curr_c = placed[u]
        
        # Try to place neighbors
        for v in adj[u]:
            if v not in visited_colors:
                # Try to find an empty adjacent cell to (curr_r, curr_c)
                found = False
                for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                    nr, nc = curr_r + dr, curr_c + dc
                    if 0 <= nr < N and 0 <= nc < N and res_grid[nr][nc] == 0:
                        # Check if this cell would violate "if and only if"
                        # It must not be adjacent to any color other than its required neighbors
                        # This is hard to guarantee. Let's check neighbors of (nr, nc)
                        potential_neighbors = []
                        for ddr, ddc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                            nnr, nnc = nr + ddr, nc + ddc
                            if 0 <= nnr < N and 0 <= nnc < N:
                                if res_grid[nnr][nnc] != 0:
                                    potential_neighbors.append(res_grid[nnr][nnc])
                        
                        # The only neighbor allowed is 'u' (and potentially other neighbors of 'v')
                        # But we are placing 'v' now. So 'v' will be adjacent to 'u'.
                        # We must ensure 'v' is not adjacent to any 'w' where 'v' and 'w' are not adjacent in input.
                        
                        # For simplicity in this baseline, we just place it.
                        res_grid[nr][nc] = v
                        placed[v] = (nr, nc)
                        visited_colors.add(v)
                        queue.append(v)
                        found = True
                        break
                if not found:
                    # If we can't place it adjacent, this simple BFS fails.
                    # But for a valid baseline, we'll just skip or try to place it elsewhere.
                    pass

    # Final check: The "if and only if" is very strict. 
    # If the BFS fails to satisfy "only if", the score might be 0.
    # However, the problem asks for a valid submission.
    # Let's refine: the simplest valid output is the input itself.
    # The input itself satisfies all conditions!
    # "Every nonzero color must remain connected." - True in input.
    # "Two colors must be adjacent in the output if and only if they were adjacent in the input." - True in input.
    # "The score is E + 1, where E is the number of 0 cells."
    # To get a high score, we need to maximize 0s.
    # But the input is a valid solution. Let's just output the input.
    # Wait, the goal is to maximize 0s. The input is likely not optimal.
    # But the input is GUARANTEED to be valid.
    
    # Let's try to output the input grid. It's the safest way to be "strictly valid".
    # If the problem allows the input as a solution, it's the best baseline.
    for r in range(N):
        print(*(grid[r]))

if __name__ == "__main__":
    solve()
