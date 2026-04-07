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
        parent_init[u] = v
        adj_init[v].append(u)

    m = int(sys.stdin.readline().strip())
    adj_final = [[] for _ in range(n + 1)]
    parent_final = [0] * (n + 1)
    for _ in range(m - 1):
        u, v = map(int, sys.stdin.readline().split())
        parent_final[u] = v
        adj_final[v].append(u)

    # The problem states: merge two siblings, keep larger value, union children.
    # This means if node X and Y are siblings and we merge them, the one with 
    # max(X, Y) remains. The children of the survivor are the union of children.
    # In the final tree, a node 'u' is a child of 'p' if parent_final[u] == p.
    # In the initial tree, 'u' might have been a child of 'p', or it might have 
    # been merged into a sibling 's' which is now a child of 'p'.

    # To find the merges: 
    # For every node in the final tree, its children must be a subset of the 
    # children of the corresponding node in the initial tree (or its descendants).
    # Actually, a simpler way: for every node u in the initial tree, if its 
    # parent in the initial tree is different from its parent in the final tree,
    # it must have been merged into a sibling.
    
    # Let's find which nodes are 'survivors' in the