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
            adj_init[u].append(v)
            adj_init[v].append(u)

        # Find root of initial tree (the one with no parent in input or just pick 1 if it's a tree)
        # Actually, the problem says 'rooted tree', but edges are given as v p (child parent).
        # Let's re-read: 'v p describing an edge'. Usually this means v is child, p is parent.
        # Let's assume p is parent of v.
        
        # Re-parsing based on 'v p' meaning v is child, p is parent
        # Wait, the problem says 'v p describing an edge'. It doesn't explicitly say v is child.
        # However, in tree problems, if it's N-1 lines, it's usually child-parent or undirected.
        # Let's assume undirected and find the root by looking at the final tree structure.
        
        # Let's refine: the input format 'v p' for N-1 lines usually implies p is parent of v.
        # Let's build adjacency lists and find roots.
        
        # Since we don't know which node is root, we look at the final tree structure.
        # But the problem says 'initial rooted tree' and 'final rooted tree'.
        # Let's assume the first node mentioned in the final tree edges is the child and second is parent.
        # Or more simply, the node that never appears as a child is the root.
        
        # Let's try building adjacency lists for both.
        adj_init = [[] for _ in range(n + 1)]
        has_parent_init = [False] * (n + 1)
        for _ in range(n - 1):
            u, v = map(int, sys.stdin.readline().split())
            # Assuming v is child, u is parent based on 'v p' description