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
    # trie[u][0] = left child, trie[u][1] = right child, trie[u][2] = count of IDs ending here
    # Using lists for speed: [left, right, end_count]
    trie = [[-1, -1, 0]]
    
    for _ in range(n):
        s = sys.stdin.readline().strip()
        u = 0
        for char in s:
            bit = int(char)
            if trie[u][bit] == -1:
                trie[u][bit] = len(trie)
                trie.append([-1, -1, 0])
            u = trie[u][bit]
        trie[u][2] += 1

    total_added = 0

    # We need to ensure that for every node u that is an end of an ID,
    # no descendant of u is an end of another ID.
    # However, the problem says: "If a reported prefix is the full final ID of a different cow..."
    # This means if ID_A is a prefix of ID_B, we must append bits to ID_A so it's no longer a prefix of ID_B.
    # Wait, the rule is: "If a reported prefix [of cow A] is the full final ID of a different cow [cow B], identity theft happened."
    # This means if ID_B is a prefix of ID_A, theft happens.
    # To prevent this, for every cow B, we must ensure no cow A has ID_B as a prefix.
    # This is equivalent to saying: no ID can be a prefix of another ID.
    # But we can append bits to the IDs. 
    # If we append bits to ID_A, it becomes longer, so it's less likely to be a prefix of ID_B.
    # If we append bits to ID_B, it becomes longer, so it's less likely to be a prefix of ID_A.
    # Actually, the condition is: for any two cows A and B, ID_A cannot be a prefix of ID_B.
    # This is the standard prefix-free code condition.
    # To minimize bits added: 
    # For each node in the Trie that marks the end of an ID, if it has descendants that are also ends of IDs,
    # we must extend the current ID until it's no longer a prefix. 
    # But we can't just extend the current ID to a