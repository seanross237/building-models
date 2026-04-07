import sys

# Increase recursion depth for deep Tries
sys.setrecursionlimit(2000000)

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    n = int(input_data[0])
    ids = input_data[1:]

    # Trie structure: each node is [child0, child1, is_terminal_count]
    # Using lists for speed in Python
    trie = [[-1, -1, 0]]
    
    for s in ids:
        curr = 0
        for char in s:
            bit = int(char)
            if trie[curr][bit] == -1:
                trie[curr][bit] = len(trie)
                trie.append([-1, -1, 0])
            curr = trie[curr][bit]
        trie[curr][2] += 1

    total_added_bits = 0

    def dfs(u, depth):
        nonlocal total_added_bits
        
        # children_results will store the depths of the 'available' terminal nodes
        # in the subtrees of u.
        # To minimize bits, we want to push terminal nodes as deep as possible.
        # However, the problem asks for the minimum bits added to ensure no ID is a prefix of another.
        # This is equivalent to ensuring that for every terminal node, no other terminal node 
        # exists in its subtree (unless we extend the current one).
        
        # Actually, the rule is: if a reported prefix is the full final ID of a different cow.
        # This means no ID can be a prefix of another ID.
        # In a Trie, this means no terminal node can be an ancestor of another terminal node.
        
        # Let's refine: For each node u, if it is a terminal node, we MUST extend it 
        # so it is no longer a prefix of any other node in its subtree.
        # Or, if there are terminal nodes in its subtree, we must extend this node.
        
        # Correct logic: 
        # For a node u, let count(u) be the number of terminal nodes in its subtree.
        # If u is a terminal node, it 'occupies' a position. To prevent it from being a prefix,
        # we must extend it to a leaf or a position where it's not a prefix.
        # But the problem says: "You may append bits to the end of each original ID".
        # This means we are modifying the original strings. 
        # If string A is a prefix of string B, we must add bits to A so it's no longer a prefix.
        
        # Let's use the property: In a Trie, if node u is terminal, and there are