import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    idx = 0
    R = int(input_data[idx]); idx += 1
    C = int(input_data[idx]); idx += 1
    N_fields = int(input_data[idx]); idx += 1
    noise = float(input_data[idx]); idx += 1
    
    # The problem description implies shapes are provided.
    # Since the exact format of shapes isn't specified, 
    # we assume a list of shapes follows.
    # For a robust baseline, we will probe cells to find oil.
    
    oil_cells = []
    
    # Simple strategy: probe every cell individually to avoid noise issues
    # in a baseline implementation.
    for r in range(R):
        for c in range(C):
            print(f"q 1 {r} {c}", flush=True)
            resp = sys.stdin.readline().strip()
            if not resp:
                break
            if resp == "1":
                oil_cells.append((r, c))
            elif resp == "0":
                pass
            else:
                # Handle potential error or unexpected input
                pass
                
    # Final submission
    if oil_cells:
        coords = " ".join([f"{r} {c}" for r, c in oil_cells])
        print(f"a {len(oil_cells)} {coords}", flush=True)
    else:
        print("a 0", flush=True)

if __name__ == "__main__":
    solve()