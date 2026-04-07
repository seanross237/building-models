import sys

# Increase recursion depth for deep Tries
sys.setrecursionlimit(2000000)

def solve():
    # Read N
    line = sys.stdin.readline()
    if not line:
        return
    n = int(line.strip())
    
    # Trie structure: nodes are dictionaries or lists
    # To save memory and time, we use a list-based Trie
    # trie[u][0] = left child, trie[u][1] = right child, is_end[u] = count of strings ending here
    
    # Given constraints (Total length 10^6), a list-based Trie is efficient.
    # Using lists for children to avoid dictionary overhead.
    max_nodes = 1000005
    trie = [[0, 0] for _ in range(max_nodes)]
    is_end = [0] * max_nodes
    nodes_cnt = 1

    for _ in range(n):
        s = sys.stdin.readline().strip()
        u = 0
        for char in s:
            bit = int(char)
            if trie[u][bit] == 0:
                trie[u][bit] = nodes_cnt
                nodes_cnt += 1
            u = trie[u][bit]
        is_end[u] += 1

    # The problem asks for minimum bits to append so no ID is a prefix of another.
    # This is equivalent to ensuring that for every node u where is_end[u] > 0,
    # there are no descendants that are also ends of strings.
    # However, the rule is: "If a reported prefix is the full final ID of a different cow, Bessie thinks identity theft happened."
    # This means if cow A's ID is a prefix of cow B's ID, theft occurs.
    # To prevent this, we must append bits to cow A so its ID is no longer a prefix of B.
    # Or append bits to B so its ID is no longer a prefix of A (impossible if A is shorter).
    # Actually, the rule is: if ID_A is a prefix of ID_B, theft occurs.
    # We want to append bits to IDs such that no ID is a prefix of another.
    # This is equivalent to saying that in the Trie, no 'end' node is an ancestor of another 'end' node.
    
    # Let's re-read: "If a reported prefix is the full final ID of a different cow..."
    # If cow A has ID '01' and cow B has ID '011', cow B can report '01' (prefix), which is cow A's ID.
    # So we must append bits to '01' to make it something like '010' or '011' (but '011' is