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

    # Mapping: which initial node corresponds to which final node
    # Since the problem guarantees a solution, we can find the mapping
    # by traversing the trees. A node in the final tree is the 'representative'
    # of a set of nodes in the initial tree.
    
    # We need to find which initial nodes are merged into which final nodes.
    # Let's find the 'representative' in the initial tree for each final node.
    # Because a merge keeps the max value, the final node value must exist in the initial tree.
    # And its parent in the final tree must be the parent (or ancestor) in the initial tree.
    
    # A more robust way: For each node in the final tree, identify its 'source' in the initial tree.
    # Since the final tree is a subset of the initial tree structure (via merges),
    # we can use the property that if node u is in the