import sys

# Increase recursion depth for deep Tries
sys.setrecursionlimit(2000000)

def solve():
    # Read N
    line = sys.stdin.readline()
    if not line:
        return
    n = int(line.strip())
    
    # Trie structure using lists for efficiency in Python
    # trie[node] = [child0, child1, is_terminal]
    # Using 0 and 1 as indices for children, and 2 for terminal flag
    trie = [[-1, -1, False]]
    
    for _ in range(n):
        s = sys.stdin.readline().strip()
        curr = 0
        for char in s:
            bit = int(char)
            if trie[curr][bit] == -1:
                trie[curr][bit] = len(trie)
                trie.append([-1, -1, False])
            curr = trie[curr][bit]
        trie[curr][2] = True

    total_cost = 0

    # The problem asks to ensure no cow's ID is a prefix of another.
    # In a Trie, this means no terminal node can be an ancestor of another terminal node.
    # If a node is terminal, we must extend its descendants so they don't fall under it.
    # However, the problem says: "If a reported prefix is the full final ID of a different cow, Bessie thinks identity theft happened."
    # This means if ID_A is a prefix of ID_B, we must append bits to ID_A so it is no longer a prefix of ID_B.
    # Wait, the rule is: "If a reported prefix [of cow B] is the full final ID of a different cow [cow A], identity theft happened."
    # So if ID_A is a prefix of ID_B, we must change ID_A or ID_B. 
    # But we can only append bits to the end of the original IDs.
    # If we append bits to ID_A, it becomes longer and might no longer be a prefix of ID_B.
    # Actually, if ID_A is a prefix of ID_B, any prefix of ID_B that is ID_A causes theft.
    # To prevent this, we must ensure that for every cow i, its ID is not a prefix of any other cow j's ID.
    # Since we can only append bits, if ID_A is a prefix of ID_B, we MUST append bits to ID_A to make it longer than ID_B? No, that's impossible if we only append to A. 
    # Let's re-read: "You may append bits to the end of each original ID... so that no cow can ever be mistaken for another."
    # If ID