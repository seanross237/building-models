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

    # A Trie node structure
    # Using lists for speed: [child0, child1, is_end_count]
    # child0/1 are indices in the nodes list
    trie = [[-1, -1, 0]]

    for s in ids:
        curr = 0
        for char in s:
            bit = 0 if char == '0' else 1
            if trie[curr][bit] == -1:
                trie[curr][bit] = len(trie)
                trie.append([-1, -1, 0])
            curr = trie[curr][bit]
        trie[curr][2] += 1

    # The problem asks for the minimum bits to append so that no ID is a prefix of another.
    # This is equivalent to ensuring that every original ID ends at a leaf in the modified Trie.
    # However, we can't just make them leaves; we need to ensure that if we append bits,
    # the new IDs are not prefixes of each other. 
    # Actually, the condition is: no cow's reported prefix is the full ID of another cow.
    # This means no ID can be a prefix of another ID.
    # If ID A is a prefix of ID B, we must append bits to A so it's no longer a prefix of B.
    # Wait, the problem says: "If a reported prefix is the full final ID of a different cow, Bessie thinks identity theft happened."
    # This means for any two cows i and j, ID_i cannot be a prefix of ID_j.
    # To achieve this, we can extend each ID such that it is not a prefix of any other.
    # This is equivalent to saying that in the Trie, no node marked as 'end of ID' is an ancestor of another 'end of ID'.
    # But we can only append bits to the *original* IDs. 
    # Let's re-read: "You may append bits to the end of each original ID... Find the minimum total number of appended bits needed so that no cow can ever be mistaken for another."
    # This means for every pair (i, j), ID_i (after appending) is not a prefix of ID_j (after appending).
    # This is equivalent to saying that all final IDs must be leaves in some Trie.
    # Actually, it's simpler: we want to extend the strings such that no string is a prefix of another.
    # In a Trie, this means no 'end-of-string' node is an ancestor of another 'end-