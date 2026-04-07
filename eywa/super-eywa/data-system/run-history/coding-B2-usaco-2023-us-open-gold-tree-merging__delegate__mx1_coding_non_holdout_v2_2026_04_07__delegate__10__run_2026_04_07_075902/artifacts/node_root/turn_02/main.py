import sys

# Increase recursion depth for deep trees
sys.setrecursionlimit(2000)

def solve():
    try:
        line = sys.stdin.readline()
        if not line: return
        T_str = line.strip()
        if not T_str: return
        T = int(T_str)
    except ValueError:
        return

    for _ in range(T):
        N = int(sys.stdin.readline().strip())
        adj_init = [[] for _ in range(N + 1)]
        parent_init = [0] * (N + 1)
        for _ in range(N - 1):
            u, v = map(int, sys.stdin.readline().split())
            adj_init[u].append(v)
            adj_init[v].append(u)
        
        parents_init = [0] * (N + 1)
        children_init = [[] for _ in range(N + 1)]
        is_child_init = [False] * (N + 1)
        adj_temp = [[] for _ in range(N + 1)]