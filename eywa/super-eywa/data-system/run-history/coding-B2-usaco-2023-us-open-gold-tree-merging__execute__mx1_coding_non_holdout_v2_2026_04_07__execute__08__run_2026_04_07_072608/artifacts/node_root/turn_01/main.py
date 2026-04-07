import sys

# Increase recursion depth for deep trees
sys.setrecursionlimit(2000)

def solve():
    try:
        line = sys.stdin.readline()
        if not line: return
        n = int(line.strip())
    except EOFError:
        return
    except ValueError:
        return

    adj_init = [[] for _ in range(n + 1)]
    parent_init = [0] * (n + 1)
    for _ in range(n - 1):
        u, v = map(int, sys.stdin.readline().split())
        adj_init[v].append(u)

    # Re-reading: 'v p' describing an edge. 
    # Let's assume the input is: node_id parent_id
    
    pass

def solve_real():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    idx = 0
    t_cases = int(input_data[idx])
    idx += 1
    
    for _ in range(t_cases):
        n = int(input_data[idx])
        idx += 1