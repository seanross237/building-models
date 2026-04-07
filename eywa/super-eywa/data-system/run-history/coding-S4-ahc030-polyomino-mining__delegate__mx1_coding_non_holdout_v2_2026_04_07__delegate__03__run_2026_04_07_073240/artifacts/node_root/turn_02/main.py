import sys

def solve():
    # 1. Read initial input
    line = sys.stdin.readline()
    if not line: return
    try:
        rows, cols, num_fields, noise = map(int, line.split())
    except ValueError: return

    shapes = []
    for _ in range(num_fields):
        line = sys.stdin.readline()
        if not line: break
        shape_data = list(map(int, line.split()))
        shapes.append(shape_data)

    # 2. Strategy: Spatial Partitioning
    oil_cells = set()
    block_size = 5
    
    for r in range(0, rows, block_size):
        for c in range(0, cols, block_size):
            query_coords = []
            for dr in range(block_size):
                for dc in range(block_size):
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < rows and 0 <= nc < cols:
                        query_coords.append(nr)
                        query_coords.append(nc)
            
            if not query_coords: continue
            
            k = len(query_coords) // 2
            print(f"q {k} " + " ".join(map(str, query_coords)), flush=True)
            
            resp = sys.stdin.readline().strip()
            if resp == 'stop': return
            
            try:
                count = int(resp)
                if count > 0:
                    for dr in range(block_size):
                        for dc in range(block_size):
                            nr, nc = r + dr, c + dc
                            if 0 <= nr < rows and 0 <= nc < cols:
                                print(f"p {nr} {nc}", flush=True)
                                p_resp = sys.stdin.readline().strip()
                                if p_resp == '1':
                                    oil_cells.add((nr, nc))
            except ValueError:
                continue

if __name__ == "__main__":
    solve()