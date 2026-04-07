import sys

def solve():
    input_data = sys.stdin.readline().split()
    if not input_data:
        return
    
    # Grid dimensions and problem parameters
    # N, M, K, noise, polyominoes
    # Note: The exact input format depends on the problem instance.
    # We assume a standard reading of N, M, K, etc.
    try:
        N = int(input_data[0])
        M = int(input_data[1])
        K = int(input_data[2])
        # noise = float(input_data[3])
        # polyominoes = input_data[4:]
    except (ValueError, IndexError):
        return

    oil_cells = []

    # Simple strategy: probe every cell individually
    # This is expensive but guaranteed to find everything if noise is low
    # or if we use a more robust method. 
    # For a baseline, we probe all cells.
    
    for r in range(1, N + 1):
        for c in range(1, M + 1):
            print(f"q 1 {r} {c}", flush=True)
            res = sys.stdin.readline().split()
            if not res:
                break
            # Assuming response is '1' for oil, '0' for no oil
            if res[0] == '1':
                oil_cells.append((r, c))
        else:
            continue
        break

    # Submit the found oil cells
    if oil_cells:
        print(f"a {len(oil_cells)}", end="")
        for r, c in oil_cells:
            print(f" {r} {c}", end="")
        print("", flush=True)
    else:
        print("a 0", flush=True)

if __name__ == "__main__":
    solve()