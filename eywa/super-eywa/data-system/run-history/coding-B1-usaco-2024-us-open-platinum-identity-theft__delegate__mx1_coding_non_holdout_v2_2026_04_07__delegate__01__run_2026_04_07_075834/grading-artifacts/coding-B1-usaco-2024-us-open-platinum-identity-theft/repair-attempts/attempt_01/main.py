import sys

# Increase recursion depth for deep Tries
sys.setrecursionlimit(2000000)

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    n = int(input_data[0])
    ids = input_data[1:]
    
    # Trie structure: nodes are lists [child0, child1, is_terminal_count]
    # Using lists for speed and memory efficiency
    # trie[u][0] = index of child 0
    # trie[u][1] = index of child 1
    # trie[u][2] = number of original IDs ending at this node
    trie = [[-1, -1, 0]]
    
    for s in ids:
        u = 0
        for char in s:
            bit = 0 if char == '0' else 1
            if trie[u][bit] == -1:
                trie[u][bit] = len(trie)
                trie.append([-1, -1, 0])
            u = trie[u][bit]
        trie[u][2] += 1

    total_cost = 0

    # We need to ensure that for every node that is a terminal node,
    # it has no descendants that are terminal nodes.
    # This is equivalent to saying every terminal node must be "pushed"
    # down to a leaf in the Trie.
    # However, the problem is: we can append bits.
    # If a node is terminal and has children, we must extend it.
    # The cost is the number of bits added.
    # A better way to view this:
    # For each node in the Trie, we want to know how many "terminal" 
    # markers are in its subtree. If a node is terminal, it must be 
    # moved to a leaf.
    # Actually, the rule is: no ID can be a prefix of another.
    # This means in the Trie, no terminal node can have a descendant that is terminal.
    # If a node is terminal and has children, we must extend the terminal node.
    # To minimize cost, we want to move terminal nodes to the "shallowest" 
    # available leaves.
    
    # Let's use a bottom-up approach.
    # For each node, we calculate how many terminal nodes are in its subtree.
    # If a node is terminal, it must be moved to a leaf.
    # But we can only move it to a leaf that is NOT an ancestor of another terminal node.
    # Wait, the rule is: "If a reported prefix is the full final ID of a different cow..."
    # This means if ID A is a prefix of ID B, theft occurs.
    # To prevent this, we must extend ID A so it's no longer a prefix of ID B.
    # The most efficient way is to extend ID A to a leaf in the Trie.
    # If we extend ID A to a leaf, it will no longer be a prefix of ID B.
    # But we must ensure the new ID A is not a prefix of some other ID C.
    # This is satisfied if we move all terminal nodes to leaves.
    
    # Correct logic:
    # Every original ID must end up at a leaf in the Trie.
    # If an original ID is at node 'u', and we move it to a leaf at depth 'd',
    # the cost is d - depth(u).
    # We want to minimize sum(d_i - depth(u_i)).
    # This is equivalent to minimizing sum(d_i) - sum(depth(u_i)).
    # Since sum(depth(u_i)) is constant, we minimize sum(d_i).
    # We have N terminal nodes. We need to pick N leaves in the Trie such that
    # each terminal node is an ancestor of its assigned leaf.
    # Actually, the terminal node doesn't have to be an ancestor.
    # We can append bits to make it a leaf.
    # If we append bits to ID A, it becomes a new string A'.
    # A' must not be a prefix of any other ID B'.
    # This is equivalent to saying all final IDs must be leaves in some Trie.
    # The original IDs are nodes in the Trie. We want to pick N leaves
    # such that each original ID is an ancestor of its assigned leaf.
    # Wait, if we append bits to ID A, the new ID A' is a descendant of A.
    # So A must be an ancestor of A'.
    # To minimize cost, for each terminal node, we want to find the nearest leaf
    # in its subtree. But we can't use the same leaf for two different IDs.
    # This is a matching problem: match each terminal node to a unique leaf in its subtree.
    # To minimize cost, we use a greedy approach with a priority queue.
    
    # Let's refine:
    # For each node, we want to know the depths of available leaves in its subtree.
    # We use a min-priority queue to store the depths of leaves available in the subtree.
    # When we encounter a terminal node, we must pick the smallest depth available
    # in its subtree and "use" it.
    
    # However, the Trie can be very large. A simple DFS with priority queue merging
    # (using the "smaller to larger" trick) will work.
    
    import heapq

    # We'll use a list of heaps. heaps[u] stores the depths of available leaves in subtree u.
    # To save memory, we'll use a single list of heaps and merge them.
    
    # But wait, the problem is simpler. We don't need to pick leaves from the *existing* Trie.
    # We can *create* new leaves by appending bits.
    # If a node has no children, it's a leaf. If it has children, we can extend it.
    # The cost to extend a node to a leaf is the distance to the nearest leaf.
    # But we can also create a new leaf by adding a bit that doesn't exist.
    # If a node has only one child, we can add a bit to create a second child (a leaf).
    # The cost to create a leaf at depth depth(u)+1 is 1.
    
    # Let's reconsider:
    # For each node, we want to find how many leaves are available in its subtree.
    # A leaf is either an existing leaf in the Trie or a new leaf we create.
    # This is still slightly wrong. Let's use the property:
    # Each terminal node must be assigned to a unique leaf.
    # A leaf can be an existing leaf in the Trie or a new leaf created by appending bits.
    # If we create a new leaf at node u, its depth is depth(u) + 1.
    # If we use an existing leaf at depth d, its depth is d.
    
    # Let's use a bottom-up approach:
    # For each node u, return a priority queue of depths of available leaves in its subtree.
    # 1. If u is a leaf (no children in Trie):
    #    The only available leaf is at depth depth(u).
    #    If u is terminal, we must "use" this leaf. But we can't use it for itself
    #    because the terminal node must be an ancestor of the leaf.
    #    Wait, if u is terminal and a leaf, the cost is 0? No, because if u is terminal,
    #    it cannot be a prefix of another. If it's a leaf, it's not a prefix of anything.
    #    So if u is terminal and a leaf, cost is 0.
    #    Wait, the problem says: "If a reported prefix is the full final ID of a different cow..."
    #    If cow A has ID "01" and cow B has ID "01", that's identity theft.
    #    But the problem says "different cow". If two cows have the same ID, 
    #    one is a prefix of the other.
    #    Actually, the constraints say "Every ID is non-empty", but doesn't say they are unique.
    #    If two cows have the same ID, we must extend one of them.
    
    # Let's use the "available leaves" idea:
    # For each node u, we want to find the depths of all available leaves in its subtree.
    # A leaf is a node with no children.
    # If a node u is terminal, it *must* be extended to a leaf.
    # If u is terminal, we take the smallest depth leaf in its subtree and "use" it.
    # If there are no leaves in its subtree, we must create one.
    # The cost to create a leaf at u is depth(u) + 1.
    # Wait, if we create a leaf at u, it's like adding a child to u.
    
    # Correct Greedy:
    # For each node u (bottom-up):
    # 1. Collect all available leaf depths from children.
    # 2. If u is terminal:
    #    - If we have available leaves in the subtree, pick the one with the smallest depth.
    #      The cost added is (smallest_depth - depth(u)).
    #      Wait, this is not quite right. The cost is (leaf_depth - original_depth).
    #      If we pick a leaf at depth 'd', the cost is d - depth(u).
    #      But we must be careful: we can only use a leaf if it's not already used.
    #    - If we have no available leaves, we must create one.
    #      The cheapest way to create a leaf is to add a bit to u, making a leaf at depth(u)+1.
    #      Cost added: (depth(u)+1) - depth(u) = 1.
    # 3. If u is not terminal:
    #    - If u is a leaf in the Trie, it's an available leaf at depth(u).
    #    - If u is not a leaf, the available leaves are those from its children.
    
    # Let's refine the "terminal" part:
    # If a node u has `count` terminal IDs, we must pick `count` leaves from its subtree.
    #
