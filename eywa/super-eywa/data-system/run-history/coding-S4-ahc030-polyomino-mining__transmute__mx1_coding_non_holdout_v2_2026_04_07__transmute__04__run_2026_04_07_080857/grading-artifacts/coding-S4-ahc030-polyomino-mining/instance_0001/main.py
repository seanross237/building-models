import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    idx = 0
    width = int(input_data[idx]); idx += 1
    height = int(input_data[idx]); idx += 1
    num_fields = int(input_data[idx]); idx += 1
    noise = float(input_data[idx]); idx += 1
    
    # The problem description implies polyominoes are provided.
    # Since the exact format of polyomino list isn't specified,
    # we assume a simple structure or skip to logic.
    # For a baseline, we will attempt to find oil by single-cell drilling.
    
    oil_cells = []
    
    for y in range(height):
        for x in range(width):
            print(f"q 1 {x} {y}", flush=True)
            res = sys.stdin.readline().strip()
            if not res:
                break
            # Assuming response is a numeric value where > 0 indicates oil
            try:
                val = float(res)
                if val > 0:
                    oil_cells.append((x, y))
            except ValueError:
                continue
                
    if oil_cells:
        ans = [f"{len(oil_cells)}"]
        for cx, cy in oil_cells:
            ans.append(f"{cx} {cy}")
        print(f"a {' '.join(ans)}", flush=True)
    else:
        print("a 0", flush=True)

if __name__ == "__main__":
    solve()