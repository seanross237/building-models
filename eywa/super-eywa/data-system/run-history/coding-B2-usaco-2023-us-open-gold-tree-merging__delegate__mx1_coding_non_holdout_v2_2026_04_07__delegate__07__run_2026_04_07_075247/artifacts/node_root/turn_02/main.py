import sys

# Increase recursion depth for deep trees
sys.setrecursionlimit(2000)

def solve():
    try:
        line = sys.stdin.readline()
        if not line: return
        n = int(line.strip())
    except ValueError:
        return

    adj_init = [[] for _ in range(n + 1)]
    parent_init = [0] * (n + 1)
    for _ in range(n - 1):
        u, v = map(int, sys.stdin.readline().split())
        adj_init[u].append(v)
        adj_init[v].append(u)

    def get_tree_structure(n, adj):
        parent = [0] * (n + 1)
        children = [[] for _ in range(n + 1)]
        visited = [False] * (n + 1)
        root = 1
        stack = [root]
        visited[root] = True
        order = []
        while stack:
            u = stack.pop()
            order.append(u)
            for v in adj[u]:
                if not visited[v]:
                    visited[v] = True
                    parent[v] = u
                    children[u].append(v)
                    stack.append(v)
        return root, parent, children, order

    root_init, parent_init, children_init, order_init = get_tree_structure(n, adj_init)

    m = int(sys.stdin.readline().strip())
    adj_final = [[] for _ in range(n + 1)]
    for _ in range(m - 1):
        u, v = map(int, sys.stdin.readline().split())