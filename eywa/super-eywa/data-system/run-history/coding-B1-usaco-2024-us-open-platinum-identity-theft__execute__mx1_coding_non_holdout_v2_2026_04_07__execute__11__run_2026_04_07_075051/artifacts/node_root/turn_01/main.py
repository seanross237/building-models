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
    # We use lists for speed in Python: trie[node] = [child0, child1, is_end]
    # child0/1 are indices in the trie list. -1 means no child.
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
    # This is equivalent to ensuring that for every node marked as 'is_end', 
    # it has no descendants that are also 'is_end'. 
    # However, the problem says: 'If a reported prefix is the full final ID of a different cow'.
    # This means if ID A is a prefix of ID B, identity theft occurs.
    # To prevent this, we must extend IDs so that no ID is a prefix of another.
    # In a Trie, this means no 'is_end' node can be an ancestor of another 'is_end' node.
    
    # We need to add bits to the existing IDs. 
    # Let's rephrase: We want to assign each original ID to a leaf in a Trie 
    # such that the path to that leaf contains the original ID as a prefix, 
    # and no two paths share a node that is the end of an ID.
    
    # Actually, the problem is simpler: we want to extend each string s_i to s'_i 
    # such that no s'_i is a prefix of s'_j.
    # This is equivalent to saying that in the Trie of the final strings, 
    # all final IDs are leaves (or at least, no final ID is an ancestor of another).
    
    # Let's count how many 'extra' nodes we need to create to make every original ID a leaf.
    # If an original ID is already a prefix of another, we MUST extend it.
    # If we extend it, we add bits. 
    
    # Wait, the rule is: 'If a reported prefix is the full final ID of a different cow'.
    # If cow A reports prefix P, and P == ID of cow