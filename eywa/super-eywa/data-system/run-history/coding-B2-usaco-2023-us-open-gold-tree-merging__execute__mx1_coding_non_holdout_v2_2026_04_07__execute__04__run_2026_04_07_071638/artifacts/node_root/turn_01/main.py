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

def main():
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
        has_parent_init = [False] * (n + 1)
        for _ in range(n - 1):
            v = int(input_data[idx])
            p = int(input_data[idx+1])
            idx += 2
            adj_init[p].append(v)
            has_parent_init[v] = True