import sys

# Increase recursion depth for deep Tries
sys.setrecursionlimit(2000000)

def solve():
    # Use fast I/O
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    n = int(input_data[0])
    ids = input_data[1:]

    # Trie structure: each node is a dictionary {bit: next_node_index}
    # is_end stores how many original IDs end at this node
    trie = [{}]
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

    # The problem asks for the minimum bits to append so that no ID is a prefix of another.
    # This means in the final Trie, every original ID must be an ancestor of a leaf,
    # and no original ID can be a leaf unless it has no descendants in the original Trie.
    # Actually, the condition "no cow can ever be mistaken for another" means:
    # For any two cows A and B, A is not a prefix of B and B is not a prefix of A.
    # This is equivalent to saying that in the Trie of final IDs, no terminal node is an ancestor of another.
    
    # Let's re-evaluate:
    # We have a Trie of original IDs. Some nodes are marked as 'end'.
    # If an 'end' node has descendants, we MUST append bits to it to move it down.
    # To minimize bits, we want to move each 'end' node to a leaf.
    # However, we can't just move it to any leaf; we must ensure the new path doesn't 
    # conflict with existing IDs.
    # Actually, the problem is: we want to pick a set of leaves in the Trie such that 
    # every original ID is a prefix of exactly one leaf, and no two leaves share a prefix.
    # Wait, that's not right. The rule is: "If a reported prefix is the full final ID of a different cow, Bessie thinks identity theft happened."
    # This means if cow A's final ID is P, no other cow B can have P as a prefix of its final ID.
    # And no cow B can have its final ID as a prefix of P.
    # This is exactly the condition that no ID is a prefix of another.
    
    # In a Trie, this means no 'end' node can be an ancestor of another 'end' node.
    # If an 'end' node has children, we must extend it.
    # To minimize cost, for each 'end' node that has children, we must pick a path 
    # downwards to a leaf that is not already "claimed" by another 'end' node.
    
    # Correct Greedy Strategy:
    # For each node in the Trie, we want to know how many "available" leaves it has in its subtree.
    # A leaf is "available" if it can be used to satisfy an 'end' node.
    # But we want to minimize the total depth added.
    # This is equivalent to: for every 'end' node, we must assign it to a leaf in its subtree.
    # If an 'end' node is at depth D, and we assign it to a leaf at depth L, cost is L-D.
    # Total cost = Sum(L_i - D_i) = Sum(L_i) - Sum(D_i).
    # To minimize this, we need to minimize Sum(L_i).
    # We must pick N distinct leaves such that each original ID is an ancestor of its assigned leaf.
    # This is a matching problem in a tree, but since it's a tree, we can use a greedy approach.
    # For each node, we want to pass up the depths of the leaves available in its subtree.
    # To minimize the sum of depths, we always pair an 'end' node with the shallowest available leaf.
    
    # Wait, the constraint is: we can only append bits. We cannot change existing bits.
    # So if we have an ID '0', and another '01', we must append something to '0' to make it '0xx' 
    # such that '0xx' is not a prefix of '01' and '01' is not a prefix of '0xx'.
    # But '0' is already a prefix of '01'. To make '0' not a prefix of '01', 
    # we must change '0' to something else? No, we can only APPEND.
    # If we append '1' to '0', we get '01', which is the same as the other cow.
    # If we append '0' to '0', we get '00', which is not a prefix of '01'.
    # So if we have '0' and '01', we can turn '0' into '00'.
    # The cost is 1.
    
    # Let's use the property: Every original ID must end up as a leaf in the Trie.
    # If an original ID is at node u, and we extend it to a leaf at node v, 
    # the cost is depth(v) - depth(u).
    # We need to select N leaves such that each original ID is an ancestor of exactly one leaf.
    # To minimize total cost, we use a greedy approach with a priority queue (min-heap) 
    # at each node to keep track of the depths of available leaves in its subtree.
    
    # Actually, a simpler way:
    # For each node, we calculate how many 'end' nodes are in its subtree.
    # If a node is an 'end' node, it MUST be satisfied by a leaf in its subtree.
    # If a node is not an 'end' node, it can either pass up leaves from its children 
    # or, if it's a leaf in the original Trie, it provides one leaf at its own depth.
    
    # Let's refine:
    # Each node u in the Trie:
    # 1. If u is a leaf in the original Trie:
    #    It provides one leaf at depth depth(u).
    # 2. If u is not a leaf:
    #    It collects all leaves from its children.
    # 3. If u is an 'end' node:
    #    It must "consume" one leaf from its subtree. To minimize cost, 
    #    it consumes the leaf with the minimum depth.
    
    # Wait, if an 'end' node is at depth D, and it consumes a leaf at depth L, 
    # the cost is L-D. But we can only append bits. 
    # If we append bits to an 'end' node to make it a leaf, that leaf 
    # cannot be one of the original leaves if that original leaf is also an 'end' node.
    # Actually, the rule is: every original ID must be transformed into a unique leaf.
    # If an original ID is already a leaf, cost is 0.
    # If an original ID is not a leaf, we must extend it to a new leaf.
    # This new leaf must not be any of the existing leaves that are 'end' nodes.
    # But we can always create a new leaf by appending a bit that doesn't exist.
    # For example, if we are at node u and need to create a leaf, we can pick a bit 
    # that is not used by any child of u.
    
    # Let's re-read: "You may append bits to the end of each original ID."
    # This means we can't change the existing IDs.
    # If we have '0' and '01', we must append something to '0'.
    # If we append '0', we get '00'. Now '00' is not a prefix of '01' and '01' is not a prefix of '00'.
    # The cost is 1.
    # If we have '0', '01', '011', we must append to '0' and '01'.
    # '0' -> '00' (cost 1)
    # '01' -> '010' (cost 1)
    # '011' -> '011' (cost 0)
    # Total cost = 2.
    
    # General rule: For every node u that is an 'end' node, if it has descendants, 
    # we must extend it to a leaf. The cost is the distance to the nearest "available" leaf.
    # A leaf is "available" if it's not an 'end' node that is already being used.
    # This is still slightly confusing. Let's simplify.
    # Every 'end' node must be a leaf. If an 'end' node is not a leaf, we must 
    # add bits to it until it becomes a leaf.
    # To minimize bits, we want to move each 'end' node to the nearest possible leaf.
    # The "available" leaves are the ones that are NOT 'end' nodes.
    # But wait, an 'end' node can be a leaf if it has no descendants.
    # If it has descendants, we must push it down.
    # The total cost is the sum of (depth of new leaf - depth of original 'end' node).
    # Each 'end' node must be assigned to a unique leaf.
    # The leaves can be:
    # 1. Original leaves that are 'end' nodes.
    # 2. Original leaves that are NOT 'end' nodes.
    # 3. New leaves we create.
    
    # Let's use the "available leaves" idea.
    # At each node u, we maintain a min-heap of depths of available leaves in its subtree.
    # 1. If u is a leaf in the Trie:
    #    If is_end[u] > 0:
    #       We have is_end[u] 'end' nodes at depth depth(u).
    #       These 'end' nodes are already leaves,
