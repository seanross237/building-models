import sys

# Increase recursion depth for deep trees
sys.setrecursionlimit(2000)

def solve():
    try:
        line = sys.stdin.readline()
        if not line:
            return
        t_str = line.strip()
        if not t_str:
            return
        t = int(t_str)
    except ValueError:
        return

    for _ in range(t):
        try:
            n = int(sys.stdin.readline().strip())
        except ValueError:
            break
        
        adj_init = [[] for _ in range(n + 1)]
        parent_init = [0] * (n + 1)
        for _ in range(n - 1):
            u, v = map(int, sys.stdin.readline().split())
            adj_init[v].append(u)
            parent_init[u] = v

        root_init = 1
        for i in range(1, n + 1):
            if parent_init[i] == 0:
                root_init = i
                break

        m = int(sys.stdin.readline().strip())
        adj_final = [[] for _ in range(n + 1)]
        parent_final = [0] * (n + 1)
        for _ in range(m - 1):
            u, v = map(int, sys.stdin.readline().split())
            adj_final[v].append(u)
            parent_final[u] = v

        root_final = 1
        for i in range(1, n + 1):
            if parent_final[i] == 0:
                root_final = i
                break