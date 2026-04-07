import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    idx = 0
    W = int(input_data[idx]); idx += 1
    H = int(input_data[idx]); idx += 1
    N = int(input_data[idx]); idx += 1
    P = float(input_data[idx]); idx += 1
    
    # The problem description says a list of polyomino shapes follows.
    # However, the exact format of the shapes list is not specified.
    # We will skip reading shapes if they aren't clearly delimited,
    # but for a robust baseline, we assume we just need to find N oil cells.
    # Since we don't know how many shapes there are, we'll try to consume
    # the rest of the input if needed, but for now, let's focus on the grid.
    
    oil_cells = []
    
    # Strategy: Brute force single-cell queries to find all oil cells.
    # This is the most reliable way to handle noise P.
    for y in range(H):
        for x in range(W):
            print(f"q 1 {x} {y}", flush=True)
            res = sys.stdin.readline().strip()
            if not res:
                break
            if res == '1':
                oil_cells.append((x, y))
            if len(oil_cells) == N:
                break
        if len(oil_cells) == N:
            break
            
    # Final submission
    output = [f"a {len(oil_cells)}"]
    for x, y in oil_cells:
        output.append(f"{x} {y}")
    print(" ".join(output), flush=True)

if __name__ == "__main__":
    solve()