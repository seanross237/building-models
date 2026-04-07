```python
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

    # Trie structure: 
    # trie[u][0] = left child, trie[u][1] = right child
    # count[u] = number of original IDs that end at or pass through node u
    # is_end[u] = number of original IDs that end exactly at node u
    
    # Pre-allocate lists to avoid repeated append calls for speed
    # Max nodes = total length of all IDs + 1
    max_nodes = sum(len(s) for s in ids) + 2
    trie = [[-1, -1] for _ in range(max_nodes)]
    is_end = [0] * max_nodes
    nodes_count = 1

    for s in ids:
        curr = 0
        for char in s:
            bit = 0 if char == '0' else 1
            if trie[curr][bit] == -1:
                trie[curr][bit] = nodes_count
                nodes_count += 1
            curr = trie[curr][bit]
        is_end[curr] += 1

    # The problem asks for the minimum bits to append so that no ID is a prefix of another.
    # This is equivalent to ensuring that in the Trie, no node marked as 'is_end' 
    # has any descendants that are also 'is_end'.
    # However, the problem allows us to append bits to *any* original ID.
    # If an ID is a prefix of another, we must extend the shorter one.
    # If multiple IDs are identical, they must all be extended to be unique.
    
    # Let's re-read: "If a reported prefix is the full final ID of a different cow, Bessie thinks identity theft happened."
    # This means if cow A's ID is P, and cow B's ID is S, and P is a prefix of S, theft occurs.
    # To prevent this, the set of final IDs must be prefix-free.
    
    # For each node in the Trie, we want to know how many IDs are "trapped" in its subtree.
    # If a node is an 'is_end' node, those IDs must be extended to become leaves.
    # If a node is not an 'is_end' node, we just pass the IDs down.
    
    # Greedy strategy:
    # For a node u, let f(u) be the minimum bits needed to make all IDs in its subtree prefix-free.
    # If is_end[u] > 0:
    #    All these IDs must be extended. To minimize bits, we extend them to be children of u.
    #    But we can only extend them to 0 or 1. If we have more than 2 IDs, we must extend them further.
    #    Actually, the problem is simpler: we want to find the minimum bits to make the set prefix-free.
    #    This is equivalent to: for every node u that is an end of an ID, we must ensure 
    #    no other ID is in its subtree.
    
    # Let's use the property: In a prefix-free set, every ID corresponds to a leaf in a Trie.
    # We want to transform the existing Trie such that all N IDs are leaves.
    # The cost is the sum of depths of the new leaves minus the sum of depths of the original IDs.
    # Wait, that's not quite right. The cost is the number of bits appended.
    # Total cost = (Sum of depths of final IDs) - (Sum of depths of original IDs).
    # To minimize total cost, we minimize the sum of depths of final IDs.
    
    # For each node u, let dp[u] be the minimum number of leaves we can have in the subtree 
    # of u such that all original IDs in u's subtree are covered.
    # This is not quite right because we need exactly N leaves.
    
    # Correct approach:
    # For each node u, let sub[u] be the number of original IDs in its subtree.
    # If u is an end node (is_end[u] > 0), these IDs MUST be extended.
    # They will effectively become leaves at depth depth(u) + 1, or deeper.
    # But we can't have two IDs at the same node.
    # Actually, if is_end[u] > 0, we must move these IDs to children.
    # If is_end[u] = k, we need to provide k distinct paths starting from u.
    
    # Let's use the "available slots" idea.
    # At any node u, we have some number of IDs that must be placed in its subtree.
    # Let count[u] be the number of original IDs that end at u or in its subtree.
    # If u is an end node, we must "push" its is_end[u] IDs down to its children.
    # The number of IDs to be distributed to children is is_end[u] + (IDs from children).
    # But we must ensure that the IDs from u don't conflict with IDs from children.
    # Actually, if we push an ID from u to a child, it's like adding 1 bit.
    
    # Let's refine:
    # For each node u, let dp[u] be the minimum bits to resolve all IDs in its subtree.
    # If u is an end node:
    #   We must extend all is_end[u] IDs. Each extension costs at least 1 bit.
    #   The IDs from is_end[u] and the IDs from children must all be distinct.
    #   This is equivalent to:
    #   Total IDs in subtree u = is_end[u] + sum(count[child])
    #   We need to distribute these 'total' IDs into the available slots in the children.
    #   A node u has at most 2 slots (child 0 and child 1).
    #   If total > 2, we must extend some IDs further down.
    
    # Let's use the property: To minimize bits, we want to keep IDs as shallow as possible.
    # For each node u, let f(u) be the number of IDs that "pass through" u to be placed in its subtree.
    # If u is an end node, we must treat its is_end[u] IDs as if they were starting from u's children.
    # So, the number of IDs to be placed in children of u is:
    #   num_to_place = is_end[u] + (IDs from child 0) + (IDs from child 1)
    #   Wait, this is not quite right. If is_end[u] > 0, we MUST extend them.
    #   If is_end[u] = 1, we can't have any other IDs in the subtree.
    #   Wait, the rule is: "If a reported prefix is the full final ID of a different cow".
    #   If cow A's ID is '10' and cow B's ID is '101', theft.
    #   If we change A to '100', then A is no longer a prefix of B.
    #   So we need to ensure no ID is a prefix of another.
    
    # Let's use the "greedy" approach for a Trie:
    # For each node u, let `needed[u]` be the number of IDs that must be placed in the subtree of u.
    # If u is an end node, we must extend all `is_end[u]` IDs.
    # This is equivalent to saying that the `is_end[u]` IDs are now "starting" from the children.
    # So, `needed[u] = is_end[u] + sum(needed[child])`.
    # But we can only have at most 2 children. If `needed[u] > 2`, we must extend some.
    # This is still not quite right. Let's use the "cost" approach.
    
    # Let's re-read: "Find the minimum total number of appended bits".
    # This is equivalent to:
    # For each node u, if it's an end node, we must move its `is_end[u]` IDs to its children.
    # If we move an ID from u to a child, it costs 1 bit.
    # If we have `is_end[u]` IDs at node u, we must distribute them to children.
    # If we have `is_end[u]` IDs and the children already have `c0` and `c1` IDs,
    # we have a total of `is_end[u] + c0 + c1` IDs to be placed in the subtree.
    # But we can only place at most 2 IDs at the next level (one in each child).
    # No, that's not right. We can place many IDs in the subtree, but they must be prefix-free.
    # The number of prefix-free IDs we can have in a subtree of height H is 2^H.
    # But we don't care about height, we care about the number of bits.
    
    # Correct logic:
    # For each node u, let `count[u]` be the number of IDs that *must* be in the subtree of u.
    # If u is an end node, we must extend all `is_end[u]` IDs.
    # Each such extension adds 1 to the cost and moves the ID to a child.
    # So, `count[u] = is_end[u] + count[child0] + count[child1]` is wrong.
    # Let's use: `count[u]` is the number of IDs that are "active" at node u.
    # If `is_end[u] > 0`, we must move all `is_end[u]` IDs to children.
    # This costs `is_end[u]` bits.
    # After moving, the number of IDs to be distributed to children is `is_end
