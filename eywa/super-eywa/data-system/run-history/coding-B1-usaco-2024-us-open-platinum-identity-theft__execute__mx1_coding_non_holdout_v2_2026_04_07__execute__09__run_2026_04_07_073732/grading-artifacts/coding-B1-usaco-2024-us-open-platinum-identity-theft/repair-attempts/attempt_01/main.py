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

    # Trie structure: nodes are lists [child0, child1, count_of_ends_in_subtree]
    # We use a flat list for speed in Python.
    # trie[u][0] = child 0 index, trie[u][1] = child 1 index, trie[u][2] = count of end-nodes in subtree
    # To save memory and time, we use three separate arrays.
    MAX_NODES = sum(len(s) for s in ids) + 2
    child0 = [-1] * MAX_NODES
    child1 = [-1] * MAX_NODES
    subtree_ends = [0] * MAX_NODES
    is_end = [0] * MAX_NODES
    
    nodes_cnt = 1
    
    for s in ids:
        curr = 0
        for char in s:
            if char == '0':
                if child0[curr] == -1:
                    child0[curr] = nodes_cnt
                    nodes_cnt += 1
                curr = child0[curr]
            else:
                if child1[curr] == -1:
                    child1[curr] = nodes_cnt
                    nodes_cnt += 1
                curr = child1[curr]
        is_end[curr] += 1

    # First pass: calculate subtree_ends
    # We can do this iteratively to avoid recursion depth issues and for speed
    # Post-order traversal using stack
    stack = [(0, False)]
    order = []
    while stack:
        u, visited = stack.pop()
        if visited:
            order.append(u)
        else:
            stack.append((u, True))
            if child1[u] != -1:
                stack.append((child1[u], False))
            if child0[u] != -1:
                stack.append((child0[u], False))
    
    for u in order:
        subtree_ends[u] = is_end[u]
        if child0[u] != -1:
            subtree_ends[u] += subtree_ends[child0[u]]
        if child1[u] != -1:
            subtree_ends[u] += subtree_ends[child1[u]]

    # The problem: We want to append bits to IDs such that no ID is a prefix of another.
    # This means in the final Trie, no node marked 'is_end' can have a descendant marked 'is_end'.
    # However, we can only append bits. This means if an original ID is a prefix of another,
    # we MUST extend the shorter one.
    # Actually, the problem is equivalent to:
    # For every node in the Trie that is an 'end' node, we must ensure it doesn't have 
    # any 'end' nodes in its subtree. But we can only extend the current 'end' node.
    # If we extend an end node, it moves down the Trie.
    # The cost is the number of bits added.
    # This is equivalent to: for every node u, if is_end[u] > 0, we must "push" 
    # these ends down to leaves or to branches such that they don't conflict.
    # But wait, the rule is: "If a reported prefix is the full final ID of a different cow".
    # This means if ID_A is a prefix of ID_B, we must extend ID_A.
    # If we extend ID_A to ID_A', then ID_A' must not be a prefix of ID_B, 
    # and ID_B must not be a prefix of ID_A'.
    # This is exactly the condition that no ID is a prefix of another.
    # In a Trie, this means no 'is_end' node is an ancestor of another 'is_end' node.
    # If a node u has is_end[u] > 0 and subtree_ends[u] > is_end[u], we must move 
    # the is_end[u] cows to children.
    # But we can only move them to children. If we move a cow from u to a child, 
    # it costs 1 bit.
    # The total cost is the sum of bits added.
    # Let dp[u] be the minimum bits to resolve all conflicts in subtree u.
    # If is_end[u] > 0:
    #   We must move all is_end[u] cows to children.
    #   Wait, if is_end[u] > 1, we have multiple cows with the same ID.
    #   They must be distinguished. To distinguish k cows at node u, we need to 
    #   send them to different branches.
    #   Actually, the problem says "different cow". If two cows have the same ID, 
    #   they are different cows. So if ID_A == ID_B, we must extend both.
    #   If we have k cows at node u, we must move them to children.
    #   The cost to move k cows from u to children is k.
    #   But we must ensure they don't collide in the children.
    
    # Correct logic:
    # For each node u, let f(u) be the number of cows that "end" at or pass through u 
    # and need to be distinguished.
    # If is_end[u] > 0:
    #   These is_end[u] cows MUST be moved to children to not be prefixes of others.
    #   Wait, if we move them to children, they are no longer prefixes of the original 
    #   IDs that were at u.
    #   Actually, the simplest way to think:
    #   Every cow must end up at a leaf in a Trie where no end-node is an ancestor of another.
    #   The cost is (final_depth - original_depth).
    #   Total cost = Sum(final_depth_i) - Sum(original_depth_i).
    #   To minimize Sum(final_depth_i), we want to place the cows as high as possible.
    #   At each node u, we have is_end[u] cows.
    #   If we have cows at u, they must be moved to children.
    #   If we have k cows at node u, we can distribute them to child0 and child1.
    #   But we can only distribute them if child0 and child1 exist.
    #   Actually, we can always "create" a child by appending a bit.
    #   This is a greedy approach:
    #   At node u, we have 'count' cows that must be placed in the subtree.
    #   If u is an end-node, we must move those cows to children.
    #   The number of cows we can "absorb" at node u is 1 (if we don't want them to be prefixes).
    #   Wait, if is_end[u] > 0, we MUST move all is_end[u] cows to children.
    #   The cost is is_end[u].
    #   Then we distribute these is_end[u] cows plus the cows from children to the children.
    #   Wait, the cows from children are already "below" u.
    #   Let's re-read: "If a reported prefix is the full final ID of a different cow, identity theft happened."
    #   This means if ID_A is a prefix of ID_B, theft.
    #   This is exactly: no ID is a prefix of another.
    #   In the Trie, this means no node with is_end[u] > 0 can have a descendant with is_end[v] > 0.
    #   If is_end[u] > 0, we must move all is_end[u] cows to children.
    #   Total cost = sum over all u where is_end[u] > 0 of (is_end[u] * 1) + (cost to resolve children).
    #   Wait, if we move a cow from u to a child, it's 1 bit. If we move it to a grandchild, it's 2 bits.
    #   This is equivalent to:
    #   For each node u, let S(u) be the number of cows that must be placed in the subtree of u.
    #   If is_end[u] > 0:
    #     We must move all is_end[u] cows to children.
    #     The number of cows to be distributed to children is is_end[u] + (cows from children).
    #     Wait, this is not quite right.
    #   Let's use the property: Total cost = Sum (final_depth_i - original_depth_i).
    #   To minimize Sum(final_depth_i), we use a greedy approach.
    #   At each node u, we have some number of cows that "must" be placed in its subtree.
    #   Let `needed[u]` be the number of cows that must be placed in the subtree of u.
    #   If u is a leaf in the original Trie, `needed[u] = is_end[u]`.
    #   If u is not a leaf:
    #     `needed[u] = is_end[u] + needed[child0] + needed[child1]`
    #   Wait, if is_end[u] > 0, these `is_end[u]` cows MUST be moved to children.
    #   So they contribute to `needed[child0]` and `needed[child1]`.
    #   But we want to minimize the total depth.
    #   At node u, we have `is_end[u]` cows that must be moved to children.
    #   We also have `needed[child0]` and `needed[child1]` cows coming from children.
    #   Total cows to be placed in children: `is_end[u] + needed[child
