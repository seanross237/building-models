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

    # A Trie node will store children and whether it's an end of an ID
    # Using lists for speed: [child0, child1, is_end]
    # child0/1 are indices in the nodes list
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

    # The problem asks for the minimum bits to append so no ID is a prefix of another.
    # This is equivalent to ensuring that in the Trie, no 'is_end' node is an ancestor of another 'is_end' node.
    # However, the problem says: "If a reported prefix is the full final ID of a different cow, Bessie thinks identity theft happened."
    # This means if ID_A is a prefix of ID_B, we must append bits to ID_A so it's no longer a prefix of ID_B.
    # Actually, the rule is: if cow A reports a prefix, and that prefix is the FULL ID of cow B, theft occurs.
    # This means no ID can be a a prefix of another ID.
    # To fix this, for every node that is an 'end' of an ID, if it has descendants that are also 'ends', 
    # we must extend the current ID until it is no longer a prefix.
    # Wait, the rule is: "If a reported prefix is the full final ID of a different cow".
    # If ID_A = '01' and ID_B = '011', cow B can report prefix '01', which is ID_A. Theft!
    # So we need to ensure no ID is a prefix of another.
    # To minimize bits, for every node that is an end-of-ID, if it has children, we must extend it.
    # But we can extend the shorter one or the longer one? 
    # Actually, we can only append bits to the *original* IDs.
    # If ID_A is a prefix of ID_B, we must append bits to ID_A to make it different from any prefix of ID_B.
    # But wait, if we append bits to ID_A, it might become a prefix of some other ID_C.
    # The