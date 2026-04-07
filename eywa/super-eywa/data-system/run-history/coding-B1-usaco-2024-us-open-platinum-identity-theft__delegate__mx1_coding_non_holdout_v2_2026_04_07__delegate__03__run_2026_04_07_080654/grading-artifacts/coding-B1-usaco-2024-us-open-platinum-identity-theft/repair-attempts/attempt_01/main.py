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

    # Trie structure using lists for efficiency
    # trie[u][0] = left child (0), trie[u][1] = right child (1)
    # is_end[u] = number of original IDs ending at node u
    # We use a large pre-allocated list to avoid repeated appends
    # Max nodes = total length + 1
    max_nodes = sum(len(s) for s in ids) + 2
    trie = [[0, 0] for _ in range(max_nodes)]
    is_end = [0] * max_nodes
    nodes_count = 1

    for s in ids:
        u = 0
        for char in s:
            bit = int(char)
            if trie[u][bit] == 0:
                trie[u][bit] = nodes_count
                nodes_count += 1
            u = trie[u][bit]
        is_end[u] += 1

    # The problem asks for the minimum bits to append so no ID is a prefix of another.
    # This is equivalent to saying every original ID must end at a leaf node.
    # However, we can't just make them leaves; we must ensure that if we extend
    # an ID, the new ID doesn't become a prefix of another.
    # Actually, the condition is: no ID is a prefix of another.
    # In a Trie, this means no node marked as 'end' can have descendants that are also 'end'.
    # But the problem says "If a reported prefix is the full final ID of a different cow".
    # This means if cow A's ID is "01" and cow B's ID is "011", B can report "01" and 
    # it matches A's full ID.
    # So, for every node u that is an 'end' of an ID, it must not have any descendants 
    # that are 'ends' of other IDs.
    # To achieve this with minimum cost, we want to push 'end' nodes down to the 
    # nearest available leaf positions.
    
    # Let's re-evaluate: We want to add bits such that for every cow i, 
    # its ID S_i is not a prefix of S_j for any j != i.
    # This is equivalent to saying that in the Trie of final IDs, 
    # no 'end' node is an ancestor of another 'end' node.
    
    # Greedy approach:
    # For each node in the Trie, we want to know how many "end" markers it needs to 
    # "push down" to become leaves.
    # A node u can "absorb" its own 'is_end' markers if it's a leaf.
    # If it's not a leaf, it must push its 'is_end' markers to its children.
    # But wait, if a node is an 'end', it MUST be a leaf in the final Trie.
    # If it has children, we must extend the ID at this node to one of the children's 
    # subtrees such that it becomes a leaf.
    
    # Correct logic:
    # For each node u, let f(u) be the number of IDs that must end in the subtree of u.
    # If u is an 'end' node, it must be extended.
    # Actually, the simplest way to think about it:
    # Every original ID must end at some node in the Trie.
    # If an ID ends at node u, and u has descendants, we must extend it.
    # To minimize cost, we want to extend it to the nearest available leaf.
    # But we can also extend it to a new branch.
    
    # Let's use the property: Total bits added = (Sum of depths of final leaf nodes) - (Sum of depths of original IDs).
    # This is not quite right because we can add new branches.
    
    # Let's use the "available slots" approach.
    # At any node u, we have some number of IDs that must end in its subtree.
    # Let count[u] be the number of original IDs that pass through or end at node u.
    # If u is an 'end' node, it must be extended to a leaf.
    # The number of leaves we can provide in the subtree of u is the number of 
    # available leaf positions.
    
    # Let's use a simpler observation:
    # We want to pick N distinct leaves in a Trie such that the sum of depths is minimized,
    # and the Trie contains all original IDs as prefixes.
    # Wait, the original IDs don't have to be prefixes of the final IDs? 
    # "You may append bits to the end of each original ID." 
    # Yes, they do. So each original ID S_i becomes S_i + T_i.
    # The final IDs must satisfy the prefix property.
    # This means in the Trie of final IDs, no node marked as an end is an ancestor of another.
    # This is exactly the same as saying all N final IDs are leaves in the Trie.
    
    # So the problem is:
    # Given a Trie of the original IDs, find N leaf nodes such that:
    # 1. Each original ID is a prefix of at least one chosen leaf.
    # 2. Each original ID is a prefix of EXACTLY one chosen leaf (to minimize cost).
    # 3. The sum of (depth(leaf_i) - depth(original_id_i)) is minimized.
    
    # This is equivalent to:
    # For each node u, let `ends[u]` be the number of original IDs that end exactly at u.
    # We need to distribute these `ends[u]` IDs to leaves in the subtree of u.
    # However, if we use a leaf in the subtree of u, it also covers all original IDs 
    # that are prefixes of u.
    
    # Let's use a bottom-up approach.
    # For each node u, let `needed[u]` be the number of IDs that must be satisfied in its subtree.
    # If `is_end[u] > 0`, these `is_end[u]` IDs must be pushed down.
    # But they can't just be pushed to any leaf; they must be pushed to leaves 
    # that are NOT ancestors of other IDs.
    # Actually, the rule is: if we extend an ID at node u, it becomes a leaf at some 
    # descendant v. This v cannot be an ancestor of any other ID.
    
    # Let's simplify:
    # We have a Trie. Some nodes are marked as 'end'.
    # We need to move each 'end' marker to a leaf such that no two markers are on the same path.
    # To minimize cost, we want to move each marker to the closest possible leaf.
    # But "closest" is tricky because moving one marker might block another.
    
    # Let's use the "available leaves" idea.
    # For a node u, let `leaves[u]` be the number of leaves in its subtree in the *original* Trie.
    # This is not quite right because we can always create new leaves.
    
    # Let's reconsider:
    # Each original ID $i$ ends at node $u_i$. We need to pick a leaf $v_i$ in the subtree of $u_i$
    # such that all $v_i$ are distinct and no $v_i$ is an ancestor of $v_j$.
    # Since they are all leaves, the second condition is automatically satisfied if they are distinct.
    # The cost is $\sum (depth(v_i) - depth(u_i))$.
    
    # This is a classic problem. For each node $u$, we want to know how many leaves 
    # are available in its subtree.
    # Let $avail[u]$ be the number of leaves we can pick in the subtree of $u$.
    # If $u$ is a leaf in the original Trie, $avail[u] = 1$.
    # If $u$ is not a leaf, $avail[u] = \max(1, \sum_{v \in children(u)} avail[v])$.
    # Wait, if $u$ is an 'end' node, it *must* be extended.
    # If $u$ is an 'end' node, it's like we have an extra ID that needs a leaf.
    # But that ID *must* be a descendant of $u$.
    
    # Let's use the following:
    # For each node $u$, let $f(u)$ be the number of IDs that end at $u$.
    # We need to satisfy all $f(u)$ IDs.
    # Let $g(u)$ be the number of IDs that are "passed up" from the children of $u$.
    # $g(u) = \sum_{v \in children(u)} g(v)$.
    # The total number of IDs that must be satisfied in the subtree of $u$ is $f(u) + g(u)$.
    # However, if $u$ is an 'end' node, we *must* push its $f(u)$ IDs to its children.
    # If $u$ has no children, we must create a new child (cost 1) and push them there.
    # But we can only push them to *available* leaf slots.
    
    # Let's use the "greedy" approach from a similar problem:
    # 1. Build the Trie.
    # 2. For each node $u$ (bottom-up):
    #    - If $u$ is a leaf in the Trie:
    #        - If $is\_end[u] > 0$:
    #            - We must extend these $is\_end[u]$ IDs.
    #            - The cost is $is\_end[u] \times 1$ (to move to a new child).
    #            - But we can't just say
