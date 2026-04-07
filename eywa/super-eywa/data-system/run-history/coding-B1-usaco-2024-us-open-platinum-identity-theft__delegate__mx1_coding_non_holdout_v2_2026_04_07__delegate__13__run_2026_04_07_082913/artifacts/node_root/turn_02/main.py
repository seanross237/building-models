import sys

# Increase recursion depth for deep Tries
sys.setrecursionlimit(2000000)

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    n = int(input_data[0])
    ids = input_data[1:]

    # Trie structure: each node is [children_dict, is_end_of_id]
    # children_dict maps '0' or '1' to the next node index
    trie = [[{}, False]]
    
    for s in ids:
        curr = 0
        for char in s:
            if char not in trie[curr][0]:
                trie[curr][0][char] = len(trie)
                trie.append([{}, False])
            curr = trie[curr][0][char]
        trie[curr][1] = True

    # To solve this, we need to ensure that for every node marked as 'is_end_of_id',
    # it has no descendants that are also 'is_end_of_id'. 
    # However, the problem states: "If a reported prefix is the full final ID of a different cow, Bessie thinks identity theft happened."
    # This means if ID A is a prefix of ID B, we must extend ID A so it is no longer a prefix of ID B.
    # In a Trie, if a node is an end-of-ID, it cannot have any descendants that are end-of-IDs.
    # Actually, the rule is: if ID_A is a prefix of ID_B, we must extend ID_A.
    # To minimize bits, for every node that is an end-of-ID and has descendants, 
    # we must extend it to a leaf. But we can also extend the descendants.
    # Wait, the rule is: no ID can be a prefix of another. 
    # This means in the Trie, no 'end-of-ID' node can be an ancestor of another 'end-of-ID' node.
    
    # Let's re-read: "If a reported prefix [of cow B] is the full final ID of a