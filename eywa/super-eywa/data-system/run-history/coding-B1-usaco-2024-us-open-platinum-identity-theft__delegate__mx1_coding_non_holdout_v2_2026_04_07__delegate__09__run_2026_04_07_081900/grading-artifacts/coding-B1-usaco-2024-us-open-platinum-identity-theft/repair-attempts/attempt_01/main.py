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

    # Trie structure using lists for efficiency in Python
    # trie[u] = [child0, child1, is_end_of_id]
    # Using a flat list to represent the trie to avoid object overhead
    # trie_nodes[u*3 + 0] = left_child
    # trie_nodes[u*3 + 1] = right_child
    # trie_nodes[u*3 + 2] = is_end_of_id (count of IDs ending here)
    
    # Pre-allocate memory for the trie to avoid repeated resizing
    # Max nodes = total length of all IDs + 1
    max_nodes = sum(len(s) for s in ids) + 2
    trie_nodes = [-1] * (max_nodes * 3)
    nodes_count = 1

    for s in ids:
        u = 0
        for char in s:
            bit = int(char)
            if trie_nodes[u * 3 + bit] == -1:
                trie_nodes[u * 3 + bit] = nodes_count
                nodes_count += 1
            u = trie_nodes[u * 3 + bit]
        trie_nodes[u * 3 + 2] += 1

    # The problem asks for the minimum bits to append so no ID is a prefix of another.
    # This means in the Trie, no node marked as 'end-of-id' can have descendants.
    # If a node u is an 'end-of-id', we must move all its 'end-of-id' markers 
    # to leaves in its subtree.
    # However, the problem says we can append bits to the *original* IDs.
    # This is equivalent to: for every node u that is an end-of-id, if it has 
    # descendants that are also end-of-ids, we must extend u.
    # Actually, the rule is: every original ID must end at a leaf in the final Trie.
    # To minimize cost, for each node u, we want to know how many "available" 
    # leaf slots are in its subtree.
    
    # Let's use a greedy approach:
    # For each node u, let f(u) be the number of IDs that must end in its subtree.
    # If u is an end-of-id, it must be pushed down.
    # The cost is the sum of (depth_of_leaf - depth_of_u).
    # A better way: For each node u, we calculate how many IDs are in its subtree.
    # If u is an end-of-id, we must move it to a child.
    # To minimize cost, we want to move it to the child that has the "shallowest" 
    # available leaf.
    
    # Correct logic:
    # For each node u, let count[u] be the number of IDs in its subtree.
    # If u is an end-of-id, we must move it to a child.
    # To minimize cost, we want to move it to a child that can accommodate it.
    # Actually, the problem is equivalent to:
    # We have a Trie. Some nodes are marked. We want to move marked nodes to leaves
    # such that no two marked nodes are on the same path.
    # The cost is the sum of distances moved.
    # This is equivalent to: for every node u, if it's an end-of-id, 
    # it must be moved to a leaf.
    # The total cost is sum_{u is end-of-id} (depth(leaf_assigned_to_u) - depth(u)).
    # This is equivalent to: sum_{u is end-of-id} depth(leaf_assigned_to_u) - sum_{u is end-of-id} depth(u).
    # To minimize this, we want to assign the "shallowest" available leaves to the 
    # "deepest" end-of-id nodes? No, that's not right.
    
    # Let's re-read: "no cow can ever be mistaken for another".
    # This means no ID is a prefix of another.
    # In the Trie, this means no end-of-id node can be an ancestor of another end-of-id node.
    # If we have an end-of-id at node u, and it has descendants, we MUST append bits to u.
    # The cost is the number of bits appended.
    # If we append bits to u to make it a leaf, we must pick a path to a leaf.
    # But we can't pick a path that is already used by another ID.
    
    # Greedy strategy:
    # For each node u, let `available_leaves(u)` be the number of leaves in its subtree.
    # If `count_ids_in_subtree(u) > available_leaves(u)`, we have a problem? No, 
    # we can always create new leaves by appending bits.
    # The real constraint: if a node u is an end-of-id, it cannot have any descendants 
    # that are end-of-ids.
    # If u is an end-of-id, we must move it to a child.
    # To minimize cost, we move it to a child that has the minimum depth to a leaf.
    # Wait, the cost is simply: for every node u that is an end-of-id, 
    # if it has descendants, we must move it.
    # Let's use the property: Total cost = sum (depth of final leaf - depth of original node).
    # This is equivalent to: for every node u, if it's an end-of-id, we must 
    # "push" it down to a child.
    # Let's track `min_depth_to_leaf(u)` for each node.
    
    # Correct Greedy:
    # For each node u, let `needed(u)` be the number of IDs that must end in its subtree.
    # If u is an end-of-id, it's one ID. Plus all IDs in its children's subtrees.
    # But if u is an end-of-id, it *cannot* be an ancestor. So we must move it.
    # The number of IDs that will end in the subtree of u is `count[u]`.
    # If u is an end-of-id, we must move it to a child.
    # The cost is 1 (to move to a child) + min_cost_to_move_from_child.
    # This is still slightly wrong. Let's use the "available slots" idea.
    # Each node u can provide some number of "slots" for IDs.
    # A leaf provides 1 slot. A node u provides `sum(slots(children))` slots.
    # If u is an end-of-id, it *must* use one slot, but it cannot be an ancestor.
    # So it must be moved to a child.
    # This is equivalent to:
    # For each node u, let `f(u)` be the number of IDs in its subtree.
    # If `u` is an end-of-id, we must move it to a child.
    # The cost is 1 + min(cost to move from child).
    # Actually, the simplest way:
    # For each node u, let `g(u)` be the minimum depth of a leaf in its subtree.
    # If u is an end-of-id, we must move it to a child.
    # The cost is 1 + min(g(child)).
    # But we must also account for the fact that we can't use the same leaf twice.
    
    # Let's use the "available leaves" approach:
    # For each node u, let `leaves(u)` be the number of leaves in its subtree.
    # If `u` is an end-of-id, we must move it to a child.
    # This is equivalent to:
    # For each node u, let `dp[u]` be the minimum cost to place all `count[u]` IDs 
    # in the subtree of `u` such that no ID is a prefix of another.
    # If `u` is an end-of-id:
    #   We must move this ID to a child.
    #   The cost is 1 + min(dp[child] + (count[child] - 1) * 0? No.)
    
    # Let's try this:
    # For each node u, let `h(u)` be the minimum depth of a leaf in its subtree.
    # If `u` is an end-of-id, we must move it to a child.
    # The cost is 1 + min(h(child)).
    # Wait, the total cost is the sum of (depth of leaf - depth of original node).
    # Let's use the property:
    # For each node u, let `count[u]` be the number of IDs in its subtree.
    # If `u` is an end-of-id, we must move it to a child.
    # The cost is 1 + min(cost to move from child).
    # Let `f(u)` be the minimum cost to satisfy all IDs in subtree `u`.
    # If `u` is not an end-of-id:
    #   `f(u) = sum(f(child))`
    #   `h(u) = min(h(child))`
    # If `u` is an end-of-id:
    #   `f(u) = sum(f(child)) + 1 + min(h(child) - depth(u) - 1)? No.`
    
    # Let's use the "available leaf depths" approach.
    # For each node u, we want to find the set of depths of leaves in its subtree.
    # To minimize cost, we want to pick the smallest depths.
