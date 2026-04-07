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
        n = int(sys.stdin.readline().strip())
        adj_init = [[] for _ in range(n + 1)]
        parent_init = [0] * (n + 1)
        for _ in range(n - 1):
            u, v = map(int, sys.stdin.readline().split())
            adj_init[u].append(v)
            adj_init[v].append(u)

        # Root the initial tree (assume 1 is root or find root)
        # The problem says 'rooted tree', but edges are given as v p (child parent).
        # Let's find the actual root (node with no parent).
        is_child_init = [False] * (n + 1)
        # Re-reading: 'v p' describes an edge. Usually v is child, p is parent.
        # Let's build adjacency and find root.
        
        # Actually, the input format 'v p' suggests p is parent of v.
        # Let's re-parse carefully.
        adj_init = [[] for _ in range(n + 1)]
        has_parent_init = [False] * (n + 1)
        for _ in range(n - 1):
            v, p = map(int, sys.stdin.readline().split())
            adj_init[p].append(v)
            has_parent_init[v] = True
        
        root_init = 1
        for i in range(1, n + 1):
            if not has_parent_init[i]:
                root_init = i
                break

        m = int(sys.stdin.readline().strip())
        adj_final = [[] for _ in range(n + 1)]
        has_parent_final = [False] * (n + 1)
