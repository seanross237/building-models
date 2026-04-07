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

    # Trie structure using lists for efficiency
    # trie[node] = [child0, child1, is_end_count]
    # Using a flat list to represent the trie to avoid object overhead
    # trie[u*3 + 0] = left child
    # trie[u*3 + 1] = right child
    # trie[u*3 + 2] = count of IDs ending here
    
    # Pre-allocate or use dynamic list. Given total length 10^6, max nodes ~10^6
    max_nodes = sum(len(s) for s in ids) + 2
    trie = [0] * (max_nodes * 3)
    nodes_count = 1

    for s in ids:
        curr = 0
        for char in s:
            bit = int(char)
            idx = curr * 3 + bit
            if trie[idx] == 0:
                trie[idx] = nodes_count
                nodes_count += 1
            curr = trie[idx]
        trie[curr * 3 + 2] += 1

    total_cost = 0

    # We need to traverse the Trie. 
    # If a node is an end-of-ID node and has children, we must extend it.
    # To minimize cost, we extend it to the nearest available leaf.
    # However, the problem is simpler: for every node that is an end-of-ID,
    # if it has descendants that are also end-of-ID, we must extend the current one.
    # Actually, the rule is: no ID can be a prefix of another.
    # This means if node U is an end-of-ID, it cannot have any descendants that are end-of-ID.
    # Wait, the rule is: "If a reported prefix is the full final ID of a different cow..."
    # This means if ID_A is a prefix of ID_B, we must extend ID_A so it's no longer a prefix.
    # To minimize cost, we extend ID_A to the shortest possible string that is not a prefix.
    # This is equivalent to saying: every end-of-