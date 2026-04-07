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
        # The problem says 'v p' describing an edge. 
        # Usually, this means v is child, p is parent.
        # Let's assume v is child, p is parent based on 'v p' notation.
        adj_init[v].append(u) # This is wrong, let's re-read.
        # 'v p' describing an edge. Let's assume p is parent of v.
        # Wait, the input says 'v p'. Let's check standard USACO format.
        # Usually it's child parent or parent child. 
        # Let's assume the second number is the parent.
        pass

    # Re-reading: 'v p' describing an edge. 
    # Let's assume the input is: child parent.
    # Actually, let's just build the adjacency list properly.
    
    # Let's restart the input reading logic.
    pass

# Since the input format 'v p' is slightly ambiguous without examples,
# but 'v' is child and 'p' is parent is common in these problems.
# Let's implement a robust parser.

def solve_real():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    idx = 0
    t_cases = int(input_data[idx])
    idx += 1
    
    for _ in range(t_cases):
        n = int(input_data[idx])
        idx += 1
        
        adj_init = [[] for _ in range(n + 1)]
        parent_init = [0] * (n + 1)