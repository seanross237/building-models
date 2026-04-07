import sys

# Increase recursion depth for deep trees
sys.setrecursionlimit(2000)

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    idx = 0
    T_cases = int(input_data[idx])
    idx += 1
    
    for _ in range(T_cases):
        N = int(input_data[idx])
        idx += 1
        
        # Initial tree: adj[parent] = [children]
        # The problem says 'v p' describing an edge. 
        # Usually, in rooted tree problems, p is parent of v.
        # However, the problem says 'initial rooted tree' and 'final rooted tree'.
        # Let's assume the input format 'v p' means p is the parent of v.
        # We need to find the root (the node that is not a child).
        
        adj_init = [[] for _ in range(N + 1)]
        has_parent_init = [False] * (N + 1)
        for _ in range(N - 1):
            v = int(input_data[idx])
            p = int(input_data[idx+1])
            idx += 2
            adj_init[p].append(v)
            has_parent_init[v] = True
            
        root_init = 1
        for i in range(1, N + 1):
            if not has_parent_init[i]:
                root_init = i
                break

        M = int(input_data[idx])
        idx += 1
        adj_final = [[] for _ in range(N + 1)]
        has_parent_final = [False] * (N + 1)
        for _ in range(M - 1):
            v = int(input_data[idx])
            p = int(input_data[idx+1])
            idx += 2
            adj_final[p].append(v)
            has_parent_final[v] = True
            
        root_final = 1
        for i in range(1, N + 1):
            if not has_parent_final[i]:
                root_final = i
                break

        # The problem states: 'One operation may merge two distinct sibling nodes. 
        # The merged