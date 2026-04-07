import sys

def solve():
    try:
        line = sys.stdin.readline()
        if not line:
            return
        parts = list(map(int, line.split()))
        if not parts:
            return
        H = parts[0]
        W = parts[1]
        N_FIELDS = parts[2]
        NOISE = parts[3]
        NUM_SHAPES = parts[4]
        oil_cells = []
        step = 2
        for r in range(0, H, step):
            for c in range(0, W, step):
                print(f'q 1 {r} {c}', flush=True)
                resp = sys.stdin.readline().strip()
                if not resp:
                    break
                if resp == '1':
                    for dr in range(-step, step + 1):
                        for dc in range(-step, step + 1):
                            nr, nc = r + dr, c + dc
                            if 0 <= nr < H and 0 <= nc < W:
                                print(f'q 1 {nr} {nc}', flush=True)
                                resp_n = sys.stdin.readline().strip()
                                if resp_n == '1':
                                    oil_cells.append((nr, nc))
            else:
                continue
            break
        oil_cells = list(set(oil_cells))
        if not oil_cells:
            print('a 0', flush=True)
        else:
            coords = []
            for cell in oil_cells:
                coords.append(f'{cell[0]} {cell[1]}')
            print(f'a {len(oil_cells)} ' + ' '.join(coords), flush=True)
    except Exception:
        pass

if __name__ == '__main__':
    solve()