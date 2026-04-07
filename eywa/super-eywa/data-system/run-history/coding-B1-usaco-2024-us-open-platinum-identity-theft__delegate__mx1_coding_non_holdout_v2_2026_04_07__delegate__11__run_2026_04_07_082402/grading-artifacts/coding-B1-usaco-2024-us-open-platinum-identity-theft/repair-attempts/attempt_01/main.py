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
    # is_end stores how many IDs end at this node
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

    total_added = 0

    def dfs(u):
        nonlocal total_added
        
        # children_results will store the number of "available" leaf paths 
        # coming up from the subtree of u that can be used to satisfy 
        # the requirement that no ID is a prefix of another.
        # However, the problem is simpler: we need to ensure that if a node 
        # is an 'end' node, it doesn't have any descendants that are also 'end' nodes.
        # But the problem says: "If a reported prefix is the full final ID of a different cow..."
        # This means if ID A is a prefix of ID B, we must extend A.
        # If we extend A, it becomes a new string. 
        # The goal is to make all IDs such that no ID is a prefix of another.
        
        # Let's redefine: For each node, we want to know how many "ends" 
        # are in its subtree. If a node is an 'end' node, it must not have 
        # any 'ends' in its subtree.
        
        # Actually, the problem is: we can append bits. 
        # This is equivalent to: in the Trie, every 'end' node must be a leaf.
        # If an 'end' node has children, we must move the 'end' status 
        # to some descendant(s) such that the total depth added is minimized.
        
        # Correct Greedy Strategy:
        # For a node u, let count(u) be the number of IDs that end at or below u.
        # If u is an 'end' node, it "consumes" one path. 
        # If u has children, the IDs in the subtrees must be pushed down.
        # But we can't just push them down; we must ensure they don't collide.
        
        # Let's use the property: To make all IDs unique prefixes, 
        # each ID must end at a leaf in the Trie.
        # If we have K IDs in a subtree rooted at u, and u is not a leaf,
        # we need to provide K distinct paths to leaves.
        
        # Wait, the problem is: "no cow can ever be mistaken for another".
        # This means no ID is a prefix of another.
        # In a Trie, this means no 'end' node is an ancestor of another 'end' node.
        
        # Let f(u) be the number of IDs that must be placed in the subtree of u.
        # If u is an 'end' node, we have one ID at u. But we can't have an 'end' 
        # node with descendants that are 'end' nodes.
        # So if u is an 'end' node, we MUST extend it.
        # But we can extend it to any child.
        
        # Let's re-read: "You may append bits to the end of each original ID."
        # This is equivalent to: for every node u that is an 'end' node, 
        # if it has any descendants that are 'end' nodes, we must extend u.
        # Or if u is an 'end' node and we want to keep it, we must extend all its descendants.
        # Actually, the simplest way to think about it:
        # Every ID must end at a leaf. If an ID ends at node u, and u is not a leaf,
        # we must extend it to some leaf in its subtree.
        # To minimize cost, we want to pick the "shallowest" available leaves.
        
        # Let's use the "available slots" approach.
        # For each node u, let `available_slots(u)` be the number of leaves in its subtree.
        # This is not quite right because we can create new leaves.
        
        # Let's use the property: In a Trie, if we want to place N IDs such that 
        # no ID is a prefix of another, we need N leaves.
        # The cost is the sum of (depth of leaf - original depth of ID).
        # This is equivalent to: Total Cost = Sum(depth of final IDs) - Sum(original depths).
        # To minimize Sum(depth of final IDs), we should pick the N shallowest 
        # available leaf positions in the Trie.
        
        # But we can only move an ID *down* its existing paths.
        # So for each node u, we know how many IDs `is_end[u]` end there.
        # We must move these `is_end[u]` IDs to leaves in the subtree of u.
        # However, we can't use the same leaf for two different IDs.
        # And if we move an ID from u to a leaf in its subtree, that leaf 
        # is now "occupied".
        
        # Let's use a bottom-up approach.
        # For each node u, let `count[u]` be the number of IDs in its subtree.
        # If `is_end[u] > 0`, we have `is_end[u]` IDs that *must* be moved 
        # to leaves in the subtree of u.
        # But wait, if `is_end[u] > 0`, we can't have any other IDs in the subtree 
        # unless we move the `is_end[u]` IDs down.
        # Actually, the rule is: no ID is a prefix of another.
        # This means if `is_end[u] > 0`, then `u` cannot have any descendants 
        # that are 'end' nodes.
        # So, if `is_end[u] > 0`, all `count[u] - is_end[u]` IDs in the subtrees 
        # must be moved to leaves, AND the `is_end[u]` IDs themselves must be 
        # moved to leaves in the subtree of u.
        # Total IDs to be placed in leaves in subtree of u: `count[u]`.
        # But we can only use leaves that are not ancestors of other IDs.
        
        # Let's simplify:
        # Every ID must end at a leaf.
        # For each node u, let `num_ids(u)` be the number of IDs that end at u.
        # We want to move these to leaves.
        # A node u can "provide" its children's leaves.
        # If u is an 'end' node, it must be extended.
        # The number of IDs that must be "pushed" from u to its children is `is_end[u]`.
        # But we also have IDs coming from the subtrees.
        
        # Let's use the "capacity" idea.
        # Each node u can support some number of IDs in its subtree.
        # If u is a leaf in the Trie, it can support 1 ID.
        # If u is not a leaf, it can support `sum(capacity(child))` IDs.
        # But if `is_end[u] > 0`, we must move those `is_end[u]` IDs to the children.
        # So the capacity of u is `sum(capacity(child))`.
        # If `is_end[u] > 0`, we must use `is_end[u]` of those capacities.
        # If `sum(capacity(child))` is less than `is_end[u]`, we must create 
        # new leaves (which costs 1 bit per new leaf).
        # Wait, the cost is the number of bits added.
        # Each time we move an ID from u to a child, it costs 1 bit.
        
        # Let `f(u)` be the number of IDs that end in the subtree of `u`.
        # Let `g(u)` be the minimum cost to resolve all prefix conflicts in the subtree of `u`.
        # This is still not quite right.
        
        # Let's use the "greedy" approach from a similar problem:
        # For each node u, let `needed(u)` be the number of IDs that must end in the subtree of `u`.
        # `needed(u) = is_end[u] + sum(needed(child))`
        # If `u` is an 'end' node, we must move all `needed(u)` IDs to the children.
        # This is not quite right because `is_end[u]` is the number of IDs that *start* at `u`.
        # If `is_end[u] > 0`, we must move all `is_end[u]` IDs to children.
        # The cost is `is_end[u] * 1` (to move them to children) + `cost(children)`.
        # But we must also ensure that the children have enough capacity.
        # The capacity of a node `u` is the number of leaves in its subtree.
        # If `is_end[u] > 0`, we must move all `is_end[u]` IDs to children.
        # This is only possible if `sum(capacity(child)) >= is_end[u] + sum(needed(child))`.
        # No, that's not it.
        
        # Let's use the correct logic:
        # For each node u, let `count[u]` be the number of IDs that end at u.
        # We want to move these `count[u]` IDs to leaves.
        # Let `dp[u]` be the
