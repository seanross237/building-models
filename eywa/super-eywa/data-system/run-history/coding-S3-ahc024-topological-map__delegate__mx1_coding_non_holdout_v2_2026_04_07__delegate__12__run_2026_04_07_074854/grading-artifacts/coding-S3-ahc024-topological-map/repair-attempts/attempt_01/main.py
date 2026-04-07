import sys

def solve():
    # Read N, M and the grid
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    N = int(input_data[0])
    M = int(input_data[1])
    grid = []
    idx = 2
    for r in range(N):
        row = []
        for c in range(N):
            row.append(int(input_data[idx]))
            idx += 1
        grid.append(row)

    # Step 1: Extract adjacency graph and connectivity
    # We need to find which colors are adjacent to which.
    # Also, we need to ensure each color is connected.
    # Since the problem asks for a valid output that preserves connectivity and adjacency,
    # a simple way to satisfy this is to find a "skeleton" of the original grid.
    # However, a very simple valid solution is to just output the original grid.
    # While not optimal for score, it is guaranteed to be valid.
    
    # To improve score slightly, we can try to find a spanning tree of each color,
    # but that is complex. Let's start with the most robust valid solution:
    # The original grid itself.
    
    for r in range(N):
        print(*(grid[r]))

if __name__ == "__main__":
    solve()
