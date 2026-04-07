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

    # The problem guarantees a solution exists. 
    # In the final tree, each node 'u' has a set of children.
    # In the initial tree, the corresponding node 'u' must have a superset of these children.
    # Any child in the initial tree that is NOT in the final tree's child list for parent 'u'
    # must have been merged into one of the children that IS in the final tree's list.
    # However, the rule is: merge two siblings, keep the larger value.
    # This implies that for a parent 'p', all its children in the initial tree that are not 
    # in the final tree must be merged into the children that are in the final tree.
    
    # Let's find the root. The root is the node with no parent.
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

    # To find the sequence, we can process nodes bottom-up.