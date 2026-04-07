import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    try:
        n = int(input_data[0])
        grid = []
        idx = 1
        for i in range(n):
            row = []
            for j in range(n):
                row.append(input_data[idx])
                idx += 1
            grid.append(row)
        
        for row in grid:
            print(" ".join(row))
    except (ValueError, IndexError):
        pass

if __name__ == "__main__":
    solve()