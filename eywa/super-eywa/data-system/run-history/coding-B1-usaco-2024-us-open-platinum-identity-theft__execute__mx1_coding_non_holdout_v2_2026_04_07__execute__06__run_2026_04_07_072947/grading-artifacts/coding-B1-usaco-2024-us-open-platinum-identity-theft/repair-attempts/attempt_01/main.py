import sys

# Increase recursion depth for deep Tries
sys.setrecursionlimit(2000000)

def solve():
    # Read N
    line = sys.stdin.readline()
    if not line:
        return
    n = int(line.strip())
    
    # Trie structure: each node is a dictionary {bit: next_node_index}
    # and a flag indicating if it's an end of an original ID.
    # Using lists for speed in Python.
    trie = [[-1, -1]]
    is_end = [False]
    
    for _ in range(n):
        s = sys.stdin.readline().strip()
        curr = 0
        for char in s:
            bit = int(char)
            if trie[curr][bit] == -1:
                trie[curr][bit] = len(trie)
                trie.append([-1, -1])
                is_end.append(False)
            curr = trie[curr][bit]
        is_end[curr] = True

    # The problem asks for the minimum bits to append so no ID is a prefix of another.
    # This is equivalent to: in the Trie, no node marked 'is_end' can be an ancestor 
    # of another node marked 'is_end'.
    # However, we can only append bits to the *original* IDs.
    # This means if an original ID is a prefix of another, we must extend the 
    # shorter one (the ancestor) until it is no longer a prefix.
    # But wait, the rule is: "If a reported prefix is the full final ID of a different cow".
    # If cow A has ID '01' and cow B has ID '011', and cow B reports '01', theft occurs.
    # To prevent this, we must extend '01' to something like '010' or '0111' (not '011').
    # Actually, the rule implies that for any two cows i and j, ID_i cannot be a prefix of ID_j.
    # To minimize cost, for every node that is an 'is_end', if it has descendants, 
    # we must extend the 'is_end' node to a leaf that is not in the subtree of any other 'is_end'.
    # Wait, the simplest way to think about it:
    # Every original ID must end at a leaf in the final Trie.
    # If an original ID is at node U, and there are other IDs in the subtree of U,
    # we must extend U to some leaf.
    # The cost is the number of bits added.
    # Let's re-read: "You may append bits to the end of each original ID."
    # This means we can only move "down" from the original nodes.
    # If node U is an end-of-string, and it has children, we must extend U to a leaf.
    # But we can't just pick any leaf; the leaf must not be an ancestor of another ID.
    # Actually, the condition "no ID is a prefix of another" is equivalent to 
    # saying every ID ends at a leaf in the Trie.
    # If we have a node that is an end-of-string, and it's not a leaf, we must extend it.
    # The cost to extend a node at depth D to a leaf at depth L is L - D.
    # To minimize total cost, we want to pick leaves such that we don't "waste" bits.
    # This is equivalent to: for every node that is an 'is_end', we must ensure 
    # it has no descendants that are also 'is_end'.
    # If a node is 'is_end', we must extend it to a leaf. 
    # If we extend it, it becomes a leaf, and its original descendants are no longer 
    # descendants of the *new* ID.
    # Wait, the problem is: we want to pick a set of leaves in the Trie such that 
    # each original ID is extended to exactly one of these leaves, and no leaf is an 
    # ancestor of another.
    # This is equivalent to: for every node that is an 'is_end', we must move it 
    # to a leaf. If we move it to a leaf, it's no longer a prefix of its original descendants.
    # The total cost is the sum of (depth of chosen leaf - depth of original node).
    # To minimize this, for each 'is_end' node, we want to find the "closest" leaf.
    # But we must ensure that the leaves we pick are "available".
    # Actually, the problem is simpler: 
    # For every node that is an 'is_end', if it has any descendants, we must extend it.
    # If we extend it to a leaf, we use (leaf_depth - node_depth) bits.
    # But we can only use leaves that are not already "claimed" by other 'is_end' nodes.
    # This is a greedy approach:
    # 1. Build the Trie.
    # 2. For each node, calculate how many leaves are in its subtree.
    # 3. For each 'is_end' node, we need to assign it to a leaf in its subtree.
    # 4. To minimize cost, we want to assign 'is_end' nodes to leaves with minimum depth.
    # However, a leaf can only be used by one 'is_end' node.
    # This is a matching problem, but since it's on a tree, we can use a greedy approach.
    # For each node, we collect the depths of all available leaves in its subtree.
    # If the node is an 'is_end', we must pick the shallowest available leaf in its subtree.
    
    # Let's refine:
    # A leaf is a node with no children in the original Trie.
    # But we can also create "new" leaves by extending an 'is_end' node.
    # Actually, the problem is: we need to pick N leaves in a Trie such that 
    # each original ID is a prefix of exactly one leaf, and no leaf is a prefix of another.
    # This is only possible if we extend each ID to a leaf.
    # The total cost is sum(depth(leaf_i) - depth(original_ID_i)).
    # To minimize this, we need to pick N leaves such that each original ID is an ancestor 
    # of exactly one leaf, and the sum of depths is minimized.
    # This is equivalent to:
    # For each node, count how many 'is_end' nodes are in its subtree.
    # Let `count[u]` be the number of 'is_end' nodes in subtree of `u`.
    # Let `leaves[u]` be the number of available leaves in subtree of `u`.
    # If `count[u] > leaves[u]`, we must create new leaves.
    # But we can't create new leaves "inside" the Trie without increasing depth.
    # Actually, the simplest way:
    # Every 'is_end' node must be extended to a leaf.
    # If an 'is_end' node is already a leaf, cost is 0.
    # If it's not a leaf, we must extend it to some leaf.
    # The total number of leaves needed is N.
    # The number of leaves available in the original Trie is the number of nodes with no children.
    # Let's use a priority queue to keep track of available leaf depths.
    
    # Correct approach:
    # 1. Build Trie.
    # 2. For each node, find how many 'is_end' nodes are in its subtree.
    # 3. For each node, find how many leaves (nodes with no children) are in its subtree.
    # 4. If a node is 'is_end', it MUST be extended to a leaf.
    # 5. This is equivalent to:
    #    Each 'is_end' node needs a leaf.
    #    We can use existing leaves or create new ones.
    #    A leaf at depth D can satisfy an 'is_end' node at depth d (d <= D) with cost D-d.
    #    Wait, if we use an existing leaf for an 'is_end' node, that leaf is "used".
    #    If we have more 'is_end' nodes than existing leaves, we must create new leaves.
    #    A new leaf can be created at depth d+1 for an 'is_end' node at depth d.
    #    Actually, the best way to create a new leaf is to just add one bit.
    #    But we must ensure the new leaf doesn't conflict.
    #    The rule is: no ID is a prefix of another.
    #    This means all N IDs must end at leaves.
    #    Total cost = sum(depth of leaf_i) - sum(depth of original_ID_i).
    #    We need to pick N leaves such that each original ID is an ancestor of exactly one leaf.
    #    This is possible if and only if we pick N leaves such that each 'is_end' node 
    #    has exactly one leaf in its subtree.
    #    This is a standard problem:
    #    For each node `u`, let `f(u)` be the set of depths of leaves in its subtree.
    #    If `u` is an `is_end` node, we must pick one depth from `f(u)` and remove it.
    #    To minimize cost, we pick the smallest depth.
    #    If `u` is not an `is_end` node, we just merge the sets from its children.
    #    If `u` is an `is_end` node and `f(u)` is empty, we must "create" a leaf at depth `depth(u)`.
    #    Wait, if we create a leaf at depth `depth(u)`, it's like adding a bit to make it a leaf.
    #    But we can't just make it a leaf if it has children. 
    #    If it has children, we must extend it to a depth where it's a leaf.
    #    The simplest way to make it a leaf is to add a bit that leads to a new branch.
    #    The cost would be 1.
    #    Actually
