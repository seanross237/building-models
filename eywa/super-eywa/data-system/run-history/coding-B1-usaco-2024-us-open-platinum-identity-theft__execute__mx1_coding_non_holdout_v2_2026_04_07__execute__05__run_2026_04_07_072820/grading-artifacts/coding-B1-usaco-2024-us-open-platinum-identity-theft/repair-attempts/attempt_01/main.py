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
    # and a flag indicating if it's the end of an original ID.
    # Using lists for speed in Python.
    # trie[u][0] = child '0', trie[u][1] = child '1', trie[u][2] = is_end_flag
    trie = [[-1, -1, 0]]
    
    for s in ids:
        u = 0
        for char in s:
            bit = int(char)
            if trie[u][bit] == -1:
                trie[u][bit] = len(trie)
                trie.append([-1, -1, 0])
            u = trie[u][bit]
        trie[u][2] += 1

    total_added = 0

    # The problem asks to ensure no ID is a prefix of another.
    # If an ID is a prefix of another, we must extend the shorter one.
    # However, the rule is: "If a reported prefix is the full final ID of a different cow..."
    # This means if cow A's final ID is a prefix of cow B's final ID, theft occurs.
    # To prevent this, for every node in the Trie that is an end-of-string,
    # it must not have any descendants that are end-of-string.
    # But we can only append bits to the *original* IDs.
    # If ID A is a prefix of ID B, we must extend A.
    # To minimize cost, we extend A to be just long enough to not be a prefix of B.
    # Actually, the rule is: for any two cows i and j, final_ID[i] is not a prefix of final_ID[j].
    # This is equivalent to saying every final ID must end at a leaf in the Trie of final IDs.
    
    # Let's re-evaluate:
    # We have a Trie of original IDs. Some nodes are marked as 'end'.
    # If a node is 'end', it cannot have any descendants that are 'end'.
    # If it does, we must extend the 'end' nodes in the subtree.
    # Wait, the problem says: "You may append bits to the end of each original ID."
    # If ID A is a prefix of ID B, we must extend A.
    # If we extend A, it becomes a longer string.
    # The goal is to make the set of strings prefix-free.
    # In a Trie, this means no 'end' node is an ancestor of another 'end' node.
    # If a node is 'end', we must move all its 'end' descendants further down.
    # But we can't move the 'end' node itself (the original ID) down, we can only add bits.
    # If we add bits to A, A becomes a longer string.
    # If A is a prefix of B, we must add bits to A so it's no longer a prefix of B.
    # The simplest way to make A not a prefix of B is to make A's length > B's length
    # and ensure they diverge. But we can only append.
    # If A is a prefix of B, any extension of A will still be a prefix of B UNLESS
    # the extension makes A longer than B.
    # Actually, if A is a prefix of B, we MUST extend A to some length L > len(B)
    # such that A is no longer a prefix of B.
    # But if we extend A, it might become a prefix of some C.
    
    # Correct logic:
    # We want to assign each original ID to a leaf in a Trie such that 
    # the path from root to the leaf contains the original ID as a prefix.
    # To minimize cost, we want the leaf to be as close to the original ID as possible.
    # This is equivalent to:
    # For each node in the Trie, let count(u) be the number of original IDs that end in the subtree of u.
    # If u is an 'end' node, it uses 1 'slot'. The remaining count(u)-1 IDs must be pushed to leaves.
    # However, if u is an 'end' node, it *cannot* be a prefix of any other ID.
    # So if u is an 'end' node, all other IDs in its subtree must be extended to be 
    # "not descendants" of u. But they are already descendants.
    # The only way to make them not descendants is to make them not have u as a prefix.
    # But they *already* have u as a prefix.
    # The only way to fix this is to extend u itself!
    # If u is an 'end' node and has descendants that are 'end' nodes, 
    # we must extend u so it's no longer a prefix of those descendants.
    # To make u not a prefix of its descendant v, we must append bits to u 
    # such that the new u is not a prefix of v.
    # This is only possible if the new u is longer than v or diverges.
    # Since we can only append, the new u will always have the old u as a prefix.
    # If u is a prefix of v, then any extension of u is either a prefix of v or v is a prefix of it.
    # To make u not a prefix of v, we must make len(u) > len(v).
    
    # Let's re-read carefully: "If a reported prefix is the full final ID of a different cow, Bessie thinks identity theft happened."
    # Let S_i be the final ID of cow i.
    # Theft if: there exists i, j (i != j) such that some prefix of S_i is equal to S_j.
    # This is exactly the definition of: S_j is a prefix of S_i.
    # So we need to ensure no S_j is a prefix of any S_i.
    # This means the set {S_i} must be prefix-free.
    # In a Trie, this means no terminal node is an ancestor of another terminal node.
    
    # For each node u in the Trie:
    # Let f(u) be the number of original IDs that end at node u.
    # Let g(u) be the number of original IDs that end in the subtree of u (including u).
    # If f(u) > 0:
    #   One of these IDs can stay at u (if we don't extend it).
    #   But if we keep one at u, no other ID can be in its subtree.
    #   So all other g(u)-1 IDs must be moved to leaves that are NOT descendants of u.
    #   But they are already descendants! The only way to "move" them is to extend u.
    #   If we extend u, it's no longer a prefix of its original descendants.
    #   Wait, if we extend u, it becomes a longer string.
    #   If we extend u to a leaf, then u is no longer a prefix of its original descendants.
    #   Actually, the most efficient way:
    #   For each node u, we want to know how many "available" leaf slots it provides.
    #   A node u provides 2 slots (0 and 1) if it's not an end-node.
    #   If it is an end-node, it "consumes" one slot and provides 0 slots for its descendants.
    #   This is not quite right. Let's use the property:
    #   Each original ID must end at some node in the Trie.
    #   If an ID ends at node u, no other ID can end at an ancestor or descendant of u.
    #   This is equivalent to: we pick N nodes in the Trie such that no node is an ancestor of another.
    #   Each picked node u must be a descendant of the original ID's node.
    #   Cost = sum (depth(picked_node_u) - depth(original_node_u)).
    
    # Let's use DP on the Trie.
    # For a node u, let dp(u) be the minimum cost to satisfy the condition for all original IDs 
    # that end in the subtree of u, given that u itself is NOT a prefix of any other ID.
    # This is still confusing. Let's simplify.
    # We have N strings. We want to extend them to S_1, ..., S_N such that they are prefix-free.
    # This is equivalent to placing N leaves in a Trie such that each S_i is a prefix of the leaf.
    # To minimize cost, we want to pick N nodes in the Trie such that:
    # 1. No node is an ancestor of another.
    # 2. For each original ID i, its node u_i is an ancestor of the chosen node v_i.
    # 3. Total cost = sum (depth(v_i) - depth(u_i)).
    
    # This is equivalent to:
    # For each node u, let count(u) be the number of original IDs that end at u.
    # We need to pick count(u) nodes in the subtree of u (including u) such that 
    # no two picked nodes have an ancestor-descendant relationship.
    # But wait, the "no ancestor-descendant" rule applies to ALL N nodes.
    # So we need to pick N nodes in the entire Trie such that no node is an ancestor of another,
    # and each original ID i is an ancestor of exactly one picked node.
    
    # Let's use the "available slots" idea.
    # A node u in the Trie can either:
    # 1. Be a terminal node for one of the original IDs. If so, it cannot have any descendants.
    # 2. Not be a terminal node. It can then provide its children as potential paths.
    
    # Let's process the Trie bottom-up.
