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
    # A merge operation: merge two siblings, keep max value, union children.
    # This means if a node in the final tree is 'X', it must have been formed
    # by merging a set of siblings in the initial tree where X is the max.
    
    # We can solve this by looking at each node in the final tree and
    # identifying which nodes in the initial tree correspond to it.
    # Since the merge operation preserves the max value, the node 'v' in the
    # final tree must be one of the nodes in the initial tree that was part of the merge.
    
    # Let's track which initial nodes are 'active' (not yet merged into something else).
    # We can use a bottom-up approach. For each node in the final tree, 
    # we find its constituent nodes in the initial tree.
    
    # However, a simpler