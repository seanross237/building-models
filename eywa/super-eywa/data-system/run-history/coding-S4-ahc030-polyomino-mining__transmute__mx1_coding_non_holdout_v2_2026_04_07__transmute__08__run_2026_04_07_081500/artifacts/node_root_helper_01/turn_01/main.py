import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    idx = 0
    grid_w = int(input_data[idx]); idx += 1
    grid_h = int(input_data[idx]); idx += 1
    num_poly = int(input_data[idx]); idx += 1
    noise = float(input_data[idx]); idx += 1
    
    # The problem description implies we need to find shapes.
    # Since we don't know the shapes' exact definitions from the prompt,
    # we implement a basic scan-and-verify strategy.
    
    found_cells = []
    
    # Simple strategy: Scan grid with single-cell drills
    # In a real scenario, we would use multi-cell queries for efficiency.
    for y in range(grid_h):
        for x in range(grid_w):
            print(f"q 1 {x} {y}", flush=True)
            res = sys.stdin.readline().strip()
            if not res:
                break
            # Assuming response is '1' for oil, '0' for empty
            if res == '1':
                found_cells.append((x, y))
        else:
            continue
        break

    # Final submission
    if found_cells:
        output = [f"a {len(found_cells)}"]
        for cx, cy in found_cells:
            output.append(f"{cx} {cy}")
        print(" ".join(output), flush=True)
    else:
        print("a 0", flush=True)

if __name__ == "__main__":
    solve()