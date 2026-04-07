import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    n = int(input_data[0])
    points = []
    idx = 1
    for _ in range(n):
        x = int(input_data[idx])
        y = int(input_data[idx+1])
        points.append((x, y))
        idx += 2
    
    edges = []
    for x, y in points:
        if x >= 0 and y >= 0:
            edges.append((0, 0, x, y))

    for e in edges:
        print(f"{e[0]} {e[1]} {e[2]} {e[3]}")

if __name__ == "__main__":
    solve()