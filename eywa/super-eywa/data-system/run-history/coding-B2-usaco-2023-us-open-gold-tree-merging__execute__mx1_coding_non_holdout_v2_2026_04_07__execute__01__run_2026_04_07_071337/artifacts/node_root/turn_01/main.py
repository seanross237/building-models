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
            parent_init[u] = v
            adj_init[v].append(u)

        M = int(input_data[idx])
        idx += 1
        adj_final = [[] for _ in range(N + 1)]
        parent_final = [0] * (N + 1)
        for _ in range(M - 1):
            u = int(input_data[idx])
            v = int(input_data[idx+1])
            idx += 2
            parent_final[u] = v
            adj_final[v].append(u)

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