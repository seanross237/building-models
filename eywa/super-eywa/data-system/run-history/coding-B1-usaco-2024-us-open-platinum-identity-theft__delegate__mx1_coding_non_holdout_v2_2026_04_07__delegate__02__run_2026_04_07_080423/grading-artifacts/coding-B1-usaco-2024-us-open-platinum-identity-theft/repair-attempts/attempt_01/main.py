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

    # Trie structure: each node is a dictionary {bit: next_node_index}
    # is_end stores the count of strings ending at this node
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

    # The problem asks for the minimum bits to append so that no string is a prefix of another.
    # This is equivalent to ensuring that in the Trie, no node marked as 'end' is an ancestor 
    # of another node marked as 'end'.
    # However, the problem states: "If a reported prefix is the full final ID of a different cow, 
    # Bessie thinks identity theft happened."
    # This means for any two cows i and j, ID_i cannot be a prefix of ID_j.
    # This is exactly the condition that no string is a prefix of another.
    
    # To minimize bits, we want to move "end" markers down to leaves.
    # But we can't just move them; we append bits. 
    # If a node is an end-of-string and has descendants that are end-of-strings, 
    # we must append bits to the current string to make it "not a prefix".
    # The most efficient way to make a string not a prefix of its descendants is to 
    # append bits until it reaches a leaf that is not part of any other string's path.
    # Actually, the problem is simpler: we need to ensure that for every node that is an 
    # end-of-string, it has no descendants that are end-of-strings.
    # If a node is an end-of-string and has children, we must extend it.
    # To minimize cost, we extend it to the nearest available leaf.
    
    # Wait, the rule is: "If a reported prefix is the full final ID of a different cow..."
    # This means if cow A's ID is "01" and cow B's ID is "011", cow A can report "01", 
    # which is the full ID of cow A, but cow B's ID is "011". 
    # If cow B reports "01", that's a prefix of B, but it's the full ID of A.
    # So we must ensure no ID is a prefix of another.
    
    # Let's re-read: "If a reported prefix is the full final ID of a different cow, 
    # Bessie thinks identity theft happened."
    # If cow A has ID "01" and cow B has ID "011".
    # If cow B reports prefix "01", it matches cow A's full ID. Identity theft!
    # So we must append bits to "01" so it's no longer a prefix of "011".
    # Or append bits to "011" so "01" is no longer a prefix? No, "01" is a prefix of "011" 
    # regardless of what we append to "011" (as long as we append to the end).
    # We must append bits to "01" to make it something like "010" or "011" (but "011" is still a prefix).
    # Actually, if we change "01" to "010", then "010" is not a prefix of "011".
    
    # Correct logic:
    # We have a Trie. Some nodes are marked as 'end'.
    # We want to add bits to some 'end' nodes such that no 'end' node is an ancestor of another.
    # For a node that is an 'end' and has descendants that are 'end's, we must push it down.
    # To minimize cost, we push it to a leaf.
    # But we can't just push it to any leaf. We need to find the minimum depth.
    # Actually, the problem is: for every node that is an 'end' and has descendants, 
    # we must add bits to it. The number of bits added is (depth of new leaf - original depth).
    # To minimize this, we want to find the "shallowest" available leaf.
    # But wait, if we move an 'end' node to a leaf, that leaf might have been used by another string.
    # This is a greedy problem on the Trie.
    
    # Let's use the property: Each string must end at a leaf.
    # If a node is an 'end' and has children, it's not a leaf.
    # We must extend it. The cost is the number of bits added.
    # Total cost = sum (depth of final leaf - original depth).
    # This is equivalent to: Total cost = (Total depth of all final leaves) - (Total depth of all original IDs).
    # To minimize this, we want to pick leaves such that their total depth is minimized, 
    # subject to the constraint that each string ends at a unique leaf and no string is a prefix of another.
    # This is equivalent to: we need to select N leaves in the Trie such that no selected leaf 
    # is an ancestor of another (which is always true for leaves) and we want to minimize 
    # the sum of depths of these N leaves, where each leaf must be a descendant of its original node.
    
    # Wait, the constraint is: "no cow can ever be mistaken for another".
    # This means for any two cows i and j, ID_i is not a prefix of ID_j.
    # This is exactly the condition that no 'end' node is an ancestor of another 'end' node.
    # In a Trie, this means all 'end' nodes must be leaves.
    # If an 'end' node is not a leaf, we must extend it to a leaf.
    # To minimize cost, we want to extend each 'end' node to the nearest available leaf.
    # However, we can't just pick any leaf. If we have two 'end' nodes, one being an ancestor 
    # of another, we must move the ancestor.
    
    # Let's use a greedy approach:
    # For each node in the Trie, calculate how many 'end' nodes are in its subtree.
    # If a node is an 'end' node, it MUST be moved to a leaf if it has any descendants.
    # But if we move it, it becomes a leaf.
    # The total number of leaves we need is N.
    # We want to pick N leaves in the Trie such that each original string is an ancestor 
    # of its assigned leaf, and no two strings share the same leaf.
    # Actually, the simplest way:
    # Every string must end at a leaf. If a string is already a leaf, cost 0.
    # If a string is not a leaf, we must extend it to a leaf.
    # To minimize cost, we want to pick N leaves such that each original string's 
    # path contains exactly one leaf, and the sum of (leaf_depth - original_depth) is minimized.
    # This is equivalent to:
    # For each node, we want to know how many leaves are available in its subtree.
    # This is a standard problem: we want to select N leaves to minimize sum of depths.
    # But the leaves must be descendants of the original strings.
    
    # Let's refine:
    # 1. Build the Trie.
    # 2. For each node, count how many original strings end there.
    # 3. We need to move all strings that are prefixes of others to leaves.
    # 4. A string at node `u` can be moved to any leaf in the subtree of `u`.
    # 5. To minimize cost, we use a greedy approach with a priority queue or similar.
    # Actually, the problem is: we need to pick N leaves such that each original string 
    # is an ancestor of its assigned leaf.
    # This is equivalent to:
    # For each node `u`, let `count[u]` be the number of original strings ending at `u`.
    # We need to distribute these `count[u]` strings to leaves in the subtree of `u`.
    # Each leaf can only take one string.
    # To minimize cost, we want to pick leaves with minimum depth.
    
    # Let's use a bottom-up approach.
    # For each node `u`, we want to find the depths of the available leaves in its subtree.
    # We can use a min-heap of depths at each node and merge them.
    # But we only need to pick the best leaves.
    
    # Wait, the problem is even simpler.
    # We need to select N leaves. Each original string `i` must be an ancestor of its leaf `L_i`.
    # This is possible if and only if the number of leaves in the subtree of `u` is at least 
    # the number of original strings in the subtree of `u`.
    # But we can always add new leaves by extending existing paths!
    # If we extend a path, we are essentially adding a new leaf.
    # The cost of adding a leaf at depth `d` is `d - original_depth`.
    # Total cost = sum(depth of chosen leaf_i) - sum(original_depth_i).
    # To minimize this, we need to minimize sum(depth of chosen leaf_i).
    # We need to pick N leaves such that each original string `i` is an ancestor of its leaf `L_i`.
    # This is equivalent to:
    # For each node `u`, let `S[u]` be the number of original strings in its subtree.
    # We must pick at least `S[u]` leaves in the subtree of `u`.
