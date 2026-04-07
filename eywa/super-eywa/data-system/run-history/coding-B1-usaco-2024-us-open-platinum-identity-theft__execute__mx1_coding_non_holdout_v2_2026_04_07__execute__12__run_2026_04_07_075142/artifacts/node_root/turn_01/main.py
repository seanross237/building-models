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
    # We also need to track if a node is the end of an ID
    trie = [{}] # list of dicts
    is_end = [False]
    
    for s in ids:
        curr = 0
        for char in s:
            bit = int(char)
            if bit not in trie[curr]:
                trie[curr][bit] = len(trie)
                trie.append({})
                is_end.append(False)
            curr = trie[curr][bit]
        is_end[curr] = True

    # The problem asks for the minimum bits to append so no ID is a prefix of another.
    # This is equivalent to ensuring that for every node that is an 'end' of an ID,
    # it has no descendants that are also 'ends' of IDs, OR we extend the current ID
    # so it is no longer a prefix. 
    # Actually, the rule is: if ID A is a prefix of ID B, identity theft occurs.
    # We want to append bits to IDs such that no ID is a prefix of another.
    # This is equivalent to saying that in the Trie of the *final* IDs, 
    # no 'end' node is an ancestor of another 'end' node.
    
    # Let's re-read: "If a reported prefix is the full final ID of a different cow, Bessie thinks identity theft happened."
    # This means if cow A's final ID is P, and cow B reports a prefix that equals P, theft occurs.
    # If cow B's final ID is P, and cow A reports a prefix that equals P, theft occurs.
    # Essentially, no final ID can be a prefix of another final ID.
    
    # To achieve this with minimum cost, we look at the Trie of the original IDs.
    # For any node that is an 'end' of an ID, if it has descendants that are also 'ends' of IDs,
    # we must extend the 'end' node (the prefix) so it's no longer a prefix.
    # However, we can't just extend the prefix; we must extend it such that it doesn't become 
    # a prefix of something else either. 
    # Wait, the problem says we can append bits to the *original* IDs.
    # If we have IDs "0" and "01", "0" is a prefix of "01". 
    # If we change "0" to "00", then "0