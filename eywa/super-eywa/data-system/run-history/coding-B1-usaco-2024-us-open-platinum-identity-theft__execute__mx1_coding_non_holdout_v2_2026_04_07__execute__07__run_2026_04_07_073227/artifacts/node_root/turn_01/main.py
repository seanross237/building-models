import sys

# Increase recursion depth for deep Tries
sys.setrecursionlimit(2000000)

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    n = int(input_data[0])
    ids = input_data[1:]

    # Trie structure: nodes are dictionaries {bit: next_node_index}
    # is_end stores the count of IDs ending at this node
    # We use lists for speed in Python
    trie = [{}] # list of dicts
    is_end = [0]
    
    for s in ids:
        curr = 0
        for char in s:
            bit = int(char)
            if bit not in trie[curr]:
                trie[curr][bit] = len(trie)
                trie.append({})
                is_end.append(0)
            curr = trie[curr][bit]
        is_end[curr] += 1

    total_appended = 0

    # We need to ensure that for every node where an ID ends, 
    # no other ID can have this node as a prefix.
    # However, the problem says: "If a reported prefix is the full final ID of a different cow, Bessie thinks identity theft happened."
    # This means if cow A's ID is a prefix of cow B's ID, we must append bits to cow A 
    # so that cow A's ID is no longer a prefix of cow B's ID.
    # Wait, the rule is: "If a reported prefix is the full final ID of a different cow".
    # If cow A reports prefix P, and P == ID of cow B, theft occurs.
    # This means no ID can be a prefix of another ID.
    # To fix this, if ID_A is a prefix of ID_B, we must append bits to ID_A 
    # until ID_A is no longer a prefix of ID_B. 
    # But we can only append bits to the END of the original IDs.
    # Actually, the rule is: if we append bits to ID_A to make it ID_A', 
    # then ID_A' must not be a prefix of any other ID_B', and no ID_B' can be a prefix of ID_A'.
    # Since we can only append, if ID_A is a prefix of ID_B, we MUST append bits to ID_A 
    # to make it longer than ID_B, or append bits to ID_B to make it not match ID_A.
    # Wait, the problem says: "You may append bits to the end of each original ID." 
    # This means we can change ID_i to ID_i + suffix_i.
    # We want to minimize sum |suffix_i| such that no ID_i