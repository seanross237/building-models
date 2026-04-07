import sys

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
        
        adj_init = [[] for _ in range(N + 1)]
        parent_init = [0] * (N + 1)
        for _ in range(N - 1):
            u = int(input_data[idx])
            v = int(input_data[idx+1])
            idx += 2
            adj_init[u].append(v)
            parent_init[v] = u
            
        adj_final = [[] for _ in range(N + 1)]
        parent_final = [0] * (N + 1)
        for _ in range(N - 1):
            u = int(input_data[idx])
            v = int(input_data[idx+1])
            idx += 2
            adj_final[u].append(v)
            parent_final[v] = u
            
        merges = []
        
        for p in range(1, N + 1):
            init_children = adj_init[p]
            final_children_set = set(adj_final[p])
            
            to_merge = []
            targets = []
            
            for child in init_children:
                if child not in final_children_set:
                    to_merge.append(child)
                else:
                    targets.append(child)
