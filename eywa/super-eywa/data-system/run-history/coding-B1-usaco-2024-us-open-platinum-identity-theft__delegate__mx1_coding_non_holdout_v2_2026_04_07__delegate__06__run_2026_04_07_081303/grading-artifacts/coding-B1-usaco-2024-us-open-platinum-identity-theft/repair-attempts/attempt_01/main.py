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
    # is_end[u] = True if an original ID ends at node u
    # We use a large pre-allocated list or append as needed.
    # Given total length 10^6, max nodes is 10^6 + 1.
    
    max_nodes = sum(len(s) for s in ids) + 2
    trie = [[0, 0] for _ in range(max_nodes)]
    is_end = [False] * max_nodes
    nodes_count = 1

    for s in ids:
        u = 0
        for char in s:
            bit = int(char)
            if trie[u][bit] == 0:
                trie[u][bit] = nodes_count
                nodes_count += 1
            u = trie[u][bit]
        is_end[u] = True

    # The problem asks for the minimum bits to append so no ID is a prefix of another.
    # This means in the final Trie, every original ID must end at a leaf node.
    # If an original ID ends at node u, and u has descendants that are also original IDs,
    # we must extend the ID at u or the descendants.
    # Actually, the rule is: if ID A is a prefix of ID B, identity theft occurs.
    # To prevent this, for every node u that is an 'end' node, it must not have any 
    # descendants that are 'end' nodes.
    # However, we can append bits to ANY ID. 
    # If we have a node u that is an 'end' node, and it has children, we MUST 
    # append bits to the ID at u to move it to a leaf.
    # But wait, the problem says: "If a reported prefix is the full final ID of a different cow..."
    # This means if cow A's ID is "01" and cow B's ID is "011", and cow B reports "01", 
    # it matches cow A's full ID.
    # So, no ID can be a prefix of another ID.
    # This is equivalent to saying: in the Trie of final IDs, no 'end' node is an ancestor of another 'end' node.
    
    # Let's re-evaluate:
    # We want to add minimum bits such that for any two IDs A and B, A is not a prefix of B.
    # In a Trie, this means no 'end' node is an ancestor of another 'end' node.
    # If we have an 'end' node u that has descendants, we must extend u to a leaf.
    # But we can also extend the descendants.
    # Actually, the simplest way to think about it:
    # For every node u that is an 'end' node, if it has any descendants that are 'end' nodes,
    # we must "push" the 'end' status of u deeper until it's a leaf, OR push the descendants.
    # But we can only append bits to the *original* IDs.
    # If we append bits to ID A, it becomes a longer string.
    # If we have IDs "0" and "01", we can change "0" to "00" (cost 1). Now "00" and "01" are prefix-free.
    # If we have "0", "01", "011", we can change "0" to "00" and "01" to "010".
    
    # Correct Greedy Strategy:
    # For each node u in the Trie:
    # Let f(u) be the minimum bits to add to the subtree at u to make all 'end' nodes in it prefix-free.
    # If u is an 'end' node:
    #    We MUST extend this ID to a leaf. To minimize cost, we find the shortest path to a leaf
    #    that doesn't pass through another 'end' node? No, that's not right.
    #    If u is an 'end' node, it cannot have any descendants that are 'end' nodes.
    #    If it does, we must extend u to a leaf. The cost is the distance to the nearest leaf.
    #    Wait, the problem is simpler:
    #    Every 'end' node must be a leaf in the final Trie.
    #    If an 'end' node u has children, we must extend it.
    #    The cost to extend u to a leaf is the distance to the nearest leaf in the current Trie.
    #    But we can also extend the children.
    
    # Let's use the property: In a prefix-free set, every string corresponds to a leaf in a binary tree.
    # We are given some nodes that *must* be leaves. If a node is an 'end' node and has children,
    # we must add bits to it to make it a leaf.
    # To minimize bits, for each 'end' node u that is not a leaf, we must add bits to make it a leaf.
    # The number of bits to add is the distance to the nearest leaf in the subtree.
    # BUT, if we add bits to u, we might "block" a path.
    # Actually, the problem is: we have a set of nodes. We want to add bits to some nodes 
    # such that no node is an ancestor of another.
    # This is equivalent to: for every 'end' node u, if u has descendants, we must extend u.
    # The cost to extend u is the number of bits we append.
    # If we extend u to a leaf, we use some bits.
    # Let's use a post-order traversal.
    # For a node u:
    # If u is an 'end' node:
    #    If u has no children, cost = 0.
    #    If u has children, we MUST extend u. The cost is 1 + (cost to make children prefix-free)? No.
    #    If u is an 'end' node, it cannot have any descendants that are 'end' nodes.
    #    If it does, we must extend u to a leaf.
    #    The minimum bits to add to u to make it a leaf is the distance to the nearest leaf.
    #    However, we can also extend the descendants.
    
    # Let's reconsider:
    # We want to select a set of leaf nodes in a (potentially expanded) Trie such that 
    # each original ID is a prefix of exactly one selected leaf.
    # This is equivalent to: for every 'end' node u, we must pick a leaf in its subtree.
    # If u is an 'end' node, we must pick a leaf that is u itself (by appending bits).
    # If we pick a leaf at depth d, and u is at depth d_u, we added (d - d_u) bits.
    # We want to minimize sum (d_i - d_u_i).
    # This is equivalent to: for every 'end' node u, we must ensure it has no descendants that are 'end' nodes.
    # If u is an 'end' node and has children, we must extend u to a leaf.
    # To minimize cost, we should extend u to the nearest leaf.
    # But wait, if we extend u to a leaf, we might use a path that was needed by a descendant.
    # Actually, the rule is: if u is an 'end' node, it cannot have any descendants that are 'end' nodes.
    # If u is an 'end' node and has children, we must extend u to a leaf.
    # The best leaf to extend u to is one that doesn't "use up" a descendant's path.
    # But the descendant's path is already there.
    # Let's use the following:
    # For each node u, let `min_dist[u]` be the distance to the nearest leaf in its subtree.
    # If u is an 'end' node and has children, we must add `min_dist[u]` bits to it.
    # BUT, we must also ensure that the descendants are handled.
    # This is still slightly wrong. Let's look at the constraints and the problem again.
    # "No cow can ever be mistaken for another."
    # This means no ID is a prefix of another.
    # If we have "0" and "01", we can:
    # 1. Change "0" to "00" (cost 1). Now we have "00" and "01".
    # 2. Change "01" to "010" (cost 1). Now we have "0" and "010". Wait, "0" is still a prefix of "010".
    # So we MUST change "0" to something that is not a prefix of "010".
    # The only way to make "0" not a prefix of "010" is to make it "00" or "011" etc.
    # In a binary Trie, if u is an 'end' node and has a child, we MUST extend u to a leaf.
    # The cost to extend u to a leaf is the distance to the nearest leaf.
    # If we extend u to a leaf, we must pick a path that does not contain any other 'end' nodes.
    # But the problem says we can append bits to *any* original ID.
    # If we have "0" and "01", we can append '0' to "0" to get "00".
    # Now "00" and "01" are prefix-free. Total cost 1.
    # If we have "0", "01", "011", we can change "0" to "00" and "01" to "010". Total cost 2.
    
    # Correct approach:
    # For each
