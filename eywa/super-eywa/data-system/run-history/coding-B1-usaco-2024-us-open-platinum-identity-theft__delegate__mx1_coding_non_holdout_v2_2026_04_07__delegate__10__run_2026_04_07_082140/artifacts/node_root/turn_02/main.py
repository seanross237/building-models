import sys

# Increase recursion depth for deep Tries
sys.setrecursionlimit(2000000)

def solve():
    # Read N
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    n = int(input_data[0])
    ids = input_data[1:]

    # Trie implementation using arrays for efficiency
    # max_nodes is total length of all IDs + 1
    max_nodes = sum(len(s) for s in ids) + 2
    
    # trie[node][0] = left child (0), trie[node][1] = right child (1)
    # Using two separate arrays for children to save memory/time
    child0 = [-1] * max_nodes
    child1 = [-1] * max_nodes
    is_end = [0] * max_nodes
    
    nodes_cnt = 1
    
    for s in ids:
        curr = 0
        for char in s:
            bit = int(char)
            if bit == 0:
                if child0[curr] == -1:
                    child0[curr] = nodes_cnt
                    nodes_cnt += 1
                curr = child0[curr]
            else:
                if child1[curr] == -1:
                    child1[curr] = nodes_cnt
                    nodes_cnt += 1
                curr = child1[curr]
        is_end[curr] += 1

    total_added_bits = 0

    # We need to traverse the Trie. 
    # If a node is an end-of-ID, and it has descendants that are end-of-IDs,
    # we must move the 'end-of-ID' status to a leaf.
    # However, the problem is simpler: if a node is an end-of-ID, 
    # it cannot have any descendants that are end-of-IDs.
    # If it does, we must extend the current ID to a leaf.
    # To minimize cost, we want to pick the 'shallowest' leaf? No, 
    # the problem asks for the minimum bits added. 
    # If an ID is a prefix of another, we must extend the shorter one.
    # To minimize cost, we extend it to the nearest available leaf in its subtree.
    
    # Let's redefine: For every node that is an end-of-