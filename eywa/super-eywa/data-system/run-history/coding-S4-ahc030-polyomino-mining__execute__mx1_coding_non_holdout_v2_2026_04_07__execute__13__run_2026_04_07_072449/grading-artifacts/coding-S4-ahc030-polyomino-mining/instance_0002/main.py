import sys

def solve():
    # Read initial input
    line = sys.stdin.readline()
    if not line:
        return
    try:
        parts = list(map(int, line.split()))
        if len(parts) < 4:
            return
        H, W, N_fields, noise_param = parts[:4]
    except ValueError:
        return

    found_cells = []
    
    for r in range(1, H + 1):
        for c in range(1, W + 1):
            print(f"q 1 {r} {c}")
            sys.stdout.flush()
            
            res = sys.stdin.readline().strip()
            if not res:
                break
            
            if res == '1':
                found_cells.append((r, c))
        else:
            continue
        break
