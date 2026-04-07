import sys

def solve():
    line = sys.stdin.readline()
    if not line:
        return
    try:
        grid_h, grid_w, num_fields, noise, polyominoes_count = map(int, line.split())
    except ValueError:
        return

    polyominoes = []
    for _ in range(polyominoes_count):
        p_line = sys.stdin.readline().split()
        if not p_line:
            break
        k = int(p_line[0])
        coords = []
        for i in range(k):
            coords.append((int(p_line[1 + 2*i]), int(p_line[2 + 2*i])))
        polyominoes.append(coords)

    found_oil = set()
    step = 2
    for r in range(0, grid_h, step):
        for c in range(0, grid_w, step):
            print(f"q 1 {r} {c}", flush=True)
            resp = sys.stdin.readline().strip()
            if not resp:
                break
            if resp == "1":
                found_oil.add((r, c))
        if not resp:
            break

    for r, c in list(found_oil):
        for poly in polyominoes:
            pass

if __name__ == "__main__":
    solve()