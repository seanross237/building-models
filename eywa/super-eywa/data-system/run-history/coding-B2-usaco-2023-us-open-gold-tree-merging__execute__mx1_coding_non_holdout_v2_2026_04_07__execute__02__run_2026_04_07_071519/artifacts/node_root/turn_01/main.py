import sys

# Increase recursion depth for deep trees
sys.setrecursionlimit(2000)

def solve():
    try:
        line = sys.stdin.readline()
        if not line: return
        N = int(line.strip())
    except EOFError:
        return
    except ValueError:
        return

    adj_init = [[] for _ in range(N + 1)]
    parent_init = [0] * (N + 1)
    for _ in range(N - 1):
        u, v = map(int, sys.stdin.readline().split())
        adj_init[v].append(u)

    def solve_real():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    idx = 0
    T_cases = int(input_data[idx])
    idx += 1
    
    for _ in range(T_cases):
        N = int(input_data[idx])
        idx += 1
        
        adj_init = [[] for _ in range(N + 1)]
        has_parent_init = [False] * (N + 1)
        for _ in range(N - 1):
            v = int(input_data[idx])
            p = int(input_data[idx+1])
            idx += 2
            adj_init[p].append(v)
            has_parent_init[v] = True
            
        root_init = 1
        for i in range(1, N + 1):
            if not has_parent_init[i]: