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
        adj_init[v].append(u)
        parent_init[u] = v

    m = int(sys.stdin.readline().strip())
    adj_final = [[] for _ in range(n + 1)]
    parent_final = [0] * (n + 1)
    for _ in range(m - 1):
        u, v = map(int, sys.stdin.readline().split())
        adj_final[v].append(u)
        parent_final[u] = v

    # Find roots
    root_init = 1
    for i in range(1, n + 1):
        if parent_init[i] == 0:
            root_init = i
            break
    
    root_final = 1
    for i in range(1, n + 1):
        if parent_final[i] == 0:
            root_final = i
            break

    # The problem guarantees a solution exists. 
    # In the final tree, each node 'u' has a set of children.
    # These children must be the result of merging some siblings in the initial tree.
    # A node 'u' in the final tree corresponds to a node in the initial tree.
    # However, the values might be different. But the problem says 'the merged node keeps the larger value'.
    # This implies that if we merge nodes, the resulting node's value is max(values).
    # Since the set of values is the same, and we only merge, the set of values in the final tree
    # is a subset of the initial values. Wait, the problem says 'the final tree uses values drawn from the same set'.
    # This means the final tree nodes are a subset of the initial nodes.
    
    # Let's track which nodes are 'active' in the current tree.
    # We can use a bottom-up approach. For