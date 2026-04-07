import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    N = int(input_data[0])
    idx = 1
    
    results = []
    for _ in range(N):
        x = float(input_data[idx])
        y = float(input_data[idx+1])
        r = float(input_data[idx+2])
        idx += 3
        
        eps = 0.000001
        results.append(f"{x} {x+eps} {y} {y+eps}")
    
    print("\n".join(results))

if __name__ == "__main__":
    solve()