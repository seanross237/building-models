import sys

# Increase recursion depth for deep trees
sys.setrecursionlimit(2000)

def solve():
    try:
        line = sys.stdin.readline()
        if not line: return
        T_str = line.strip()
        if not T_str: return
        T = int(T_str)
    except EOFError:
        return
    except ValueError:
        return

    for _ in range(T):
        line = sys.stdin.readline()
        while not line or not line.strip():
            line = sys.stdin.readline()
        N = int(line.strip())
        
        adj_init = [[] for _ in range(N + 1)]
        parent_init = [0] * (N + 1)
        for _ in range(N - 1):
            u, v = map(int, sys.stdin.readline().split())
            adj_init[v].append(u)
            parent_init[u] = v
            
        line = sys.stdin.readline()
        while not line or not line.strip():
            line = sys.stdin.readline()
        M = int(line.strip())
        
        adj_final = [[] for _ in range(N + 1)]
        parent_final = [0] * (N + 1)
        for _ in range(M - 1):
            u, v = map(int, sys.stdin.readline().split())
            adj_final[v].append(u)
            parent_final[u] = v

        # Find roots
        root_init = 1
        for i in range(1, N + 1):
            if parent_init[i] == 0:
                root_init = i
                break
        
        root_final = 1
        for i in range(1, N + 1):
            if parent_final[i] == 0:
                root_final = i
                break

        # Map initial nodes to final nodes
        # Since it's guaranteed a solution exists, each final node 
        # corresponds to a set of initial nodes that form a subtree structure.
        # We can find which initial node belongs to which final node by 
        # observing that if node u is in final node F, then parent(u) in init
        # must be in parent(F) in final, or F is root.
        
        final_of_init = [0] * (N + 1)
        