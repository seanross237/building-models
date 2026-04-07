import sys

# Increase recursion depth for deep trees
sys.setrecursionlimit(2000)

def solve():
    try:
        line = sys.stdin.readline()
        if not line:
            return
        n = int(line.strip())
    except ValueError:
        return

    adj_init = [[] for _ in range(n + 1)]
    parent_init = [0] * (n + 1)
    for _ in range(n - 1):
        u, v = map(int, sys.stdin.readline().split())
        adj_init[u].append(v)
        adj_init[v].append(u)

    # Find root of initial tree (the one that is not a child in the final tree or simply the one with no parent in the input structure)
    # However, the problem says 'rooted tree'. Usually, the first node or a specific node is root. 
    # Let's find the root by finding the node that is not a child in the edge list if provided as (child, parent).
    # The input says 'v p' describing an edge. Usually this means v is child, p is parent.
    
    # Re-reading: 'v p' describing an edge. Let's assume p is parent of v.
    # Let's reconstruct the tree structure.
    
    # Since we don't know the root, but we know it's a rooted tree, we can find the root by finding the node with no parent.
    # Wait, the input format 'v p' for N-1 lines implies p is the parent of v.
    
    # Let's re-parse carefully.
    # For initial tree:
    init_parents = [0] * (n + 1)
    init_children = [[] for _ in range(n + 1)]
    for _ in range(n - 1):
        v, p = map(int, sys.stdin.readline().split())
        init_parents[v] = p
        init_children[p].append(v)
    
    root_init = 0
    for i in range(1, n + 1):
        if init_parents[i] == 0:
            root_init = i
            break

    m_line = sys.stdin.readline().strip()
    if not m_line:
        return
    m = int(m_line)
    
    final_parents =