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

    # Trie structure: each node is a list [child0, child1, is_end_of_id]
    # Using lists for speed in Python
    trie = [[-1, -1, False]]

    for s in ids:
        curr = 0
        for char in s:
            bit = int(char)
            if trie[curr][bit] == -1:
                trie[curr][bit] = len(trie)
                trie.append([-1, -1, False])
            curr = trie[curr][bit]
        trie[curr][2] = True

    total_bits_added = 0

    # We need to ensure that no ID is a prefix of another.
    # If an ID ends at a node, no other ID can pass through this node.
    # However, the problem says: "If a reported prefix is the full final ID of a different cow..."
    # This means if ID_A is a prefix of ID_B, we must append bits to ID_A so it's no longer a prefix.
    # Wait, the rule is: "If a reported prefix [of cow B] is the full final ID of a different cow [cow A], identity theft happened."
    # This means if ID_A is a prefix of ID_B, we must append bits to ID_A so that ID_A is no longer a prefix of ID_B.
    # Actually, the problem says we can append bits to the end of EACH original ID.
    # Let's re-read: "You may append bits to the end of each original ID... so that no cow can ever be mistaken for another."
    # A cow B is mistaken for cow A if a prefix of B is the full ID of A.
    # This is exactly the definition of A being a prefix of B.
    # To prevent this, for every pair (A, B) where A is a prefix of B, we must append bits to A or B.
    # But we want to minimize total bits. If A is a prefix of B, we can append bits to A to make it not a prefix.
    # Actually, if we append bits to A, it becomes longer, so it might still be a prefix of B.
    # The only way to stop A from being a prefix of B is to make A's final ID not match any prefix of B.
    # But B's prefixes are fixed by B's final ID. 
    # Let's re-read carefully: "Each cow may report any prefix of its final ID... If a reported prefix is the