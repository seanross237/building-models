import sys

# Increase recursion depth for deep Tries
sys.setrecursionlimit(2000000)

def solve():
    # Read N
    line = sys.stdin.readline()
    if not line:
        return
    n = int(line.strip())
    
    # Trie structure: each node is a dictionary {bit: next_node_index}
    # is_terminal stores how many original IDs end at this node
    trie = [{}]
    is_terminal = [0]
    
    for _ in range(n):
        s = sys.stdin.readline().strip()
        curr = 0
        for char in s:
            bit = int(char)
            if bit not in trie[curr]:
                trie[curr][bit] = len(trie)
                trie.append({})
                is_terminal.append(0)
            curr = trie[curr][bit]
        is_terminal[curr] += 1

    # The problem asks to append bits so that no ID is a prefix of another.
    # This means in the final Trie, no terminal node can be an ancestor of another terminal node.
    # If a node is terminal and has descendants that are terminal, we must "push" the 
    # terminal status of the current node down to a leaf.
    # However, the problem says "You may append bits to the end of each original ID".
    # This means if ID A is a prefix of ID B, we must append bits to A.
    # To minimize cost, we want to move the terminal marker of A to a position 
    # that is not an ancestor of any other terminal marker.
    # The cost to move a terminal marker from node u to a descendant leaf is the depth difference.
    # But we can't just move it; we are adding bits to the original string.
    # If we add k bits to string S, it becomes a string of length len(S) + k.
    # The goal is to ensure no string is a prefix of another.
    # This is equivalent to saying every terminal node must be a leaf in the Trie 
    # formed by the final strings.
    
    # Let's re-evaluate:
    # For every node in the Trie, let count[u] be the number of original IDs that 
    # end at or below node u.
    # If a node u is a terminal node (is_terminal[u] > 0), and it has descendants 
    # that are also terminal, we must extend the IDs ending at u.
    # Actually, the rule is: if we have multiple IDs that are prefixes of each other,
    # we must extend the shorter ones.
    # If we have k IDs ending at node u, and there are some IDs in the subtree of u,
    # we must extend all k IDs such that they are no longer prefixes.
    # The most efficient way is to extend them to become leaves.
    # But we can't "reuse" the same path for all k IDs if they are to be distinct.
    # Wait, the problem says "no cow can ever be mistaken for another".
    # This means if cow A's ID is a prefix of cow B's ID, theft happens.
    # This must hold for the FINAL IDs.
    # So in the final set of IDs, no ID is a prefix of another.
    # This means every final ID must correspond to a leaf in the Trie of final IDs.
    
    # Let's use DP on the Trie.
    # For a node u, let f(u) be the minimum bits to add to all IDs in the subtree of u
    # such that no ID in the subtree is a prefix of another, AND no ID in the subtree
    # is a prefix of any ID outside the subtree.
    # This is slightly wrong. The IDs outside the subtree are already handled.
    # The condition "no ID is a prefix of another" is equivalent to:
    # Every terminal node must be a leaf.
    
    # Let's count how many "terminal" markers we have in the subtree of u.
    # Let subtree_terminals[u] be the number of original IDs that end in the subtree of u.
    # If we are at node u, and is_terminal[u] > 0:
    # We have 'is_terminal[u]' IDs that end exactly here.
    # We also have 'subtree_terminals[u] - is_terminal[u]' IDs in the subtrees.
    # To make the 'is_terminal[u]' IDs not prefixes, we must extend them.
    # To minimize cost, we extend them to the nearest available leaf positions.
    # But we can also extend the IDs in the subtrees.
    
    # Correct approach:
    # Each original ID must end up at some node in the Trie such that no node is an ancestor of another.
    # This is equivalent to picking N distinct leaves in a Trie.
    # However, we can only add bits to the existing IDs.
    # This means if an ID is at node u, we can move it to any descendant node v.
    # The cost is depth(v) - depth(u).
    # We want to pick N nodes {v_1, ..., v_N} such that:
    # 1. v_i is a descendant of the original node u_i.
    # 2. No v_i is an ancestor of v_j.
    # 3. Sum (depth(v_i) - depth(u_i)) is minimized.
    
    # This is equivalent to:
    # For each node u, let count[u] be the number of original IDs ending at u.
    # We need to distribute these count[u] markers to leaves in the subtree.
    # But we can also use the existing terminal markers in the subtrees.
    # Actually, the total number of markers is N.
    # We need to pick N nodes such that no node is an ancestor of another.
    # The best nodes to pick are the "deepest" possible nodes? No, the "shallowest" 
    # possible nodes that satisfy the condition.
    # Wait, if we pick a node u, we can't pick any of its descendants or ancestors.
    # This is exactly the problem of finding N nodes in the Trie such that no node 
    # is an ancestor of another, minimizing the sum of (depth(v_i) - depth(u_i)).
    
    # Let's use the property:
    # For any node u, let S(u) be the number of original IDs in its subtree.
    # If we decide that the "terminal" nodes in the subtree of u will be 
    # some set of nodes, the number of such nodes must be exactly S(u).
    # If we pick a node u to be a terminal node, we can't pick any other node in its subtree.
    # So if we pick u, we get 1 terminal node, and we must have S(u) = 1.
    # If S(u) > 1, we cannot pick u. We must pick nodes in its children's subtrees.
    # If we pick nodes in the subtrees of children c1, c2, ..., ck, 
    # the total number of terminal nodes will be sum(S(ci)).
    # If sum(S(ci)) < S(u), it's impossible? No, because S(u) = is_terminal[u] + sum(S(ci)).
    # If is_terminal[u] > 0, then S(u) > sum(S(ci)).
    # This means if is_terminal[u] > 0, we MUST extend the is_terminal[u] IDs 
    # to some descendants.
    
    # Let's re-read: "If a reported prefix is the full final ID of a different cow, Bessie thinks identity theft happened."
    # This means if ID_A is a prefix of ID_B, theft happens.
    # This is exactly: no ID is a prefix of another.
    # So we need to pick N nodes such that no node is an ancestor of another.
    # Let's say we pick a set of nodes V = {v_1, ..., v_N}.
    # The cost is sum_{i=1}^N (depth(v_i) - depth(u_i)).
    # To minimize this, we want to pick v_i as close to u_i as possible.
    # For a node u, if is_terminal[u] > 0, we must move these is_terminal[u] IDs 
    # to some descendants.
    # Let's use DP: dp[u] = minimum cost to resolve all IDs in the subtree of u.
    # If is_terminal[u] > 0:
    # We have is_terminal[u] IDs that must be moved to descendants.
    # The total number of IDs to be placed in the subtree is S(u).
    # The number of available "slots" in the subtrees is sum(S(child)).
    # But we can't just use slots. We need to place exactly S(u) IDs.
    # This is only possible if we extend the is_terminal[u] IDs.
    # Each such ID will eventually end up at some leaf.
    # The total cost is:
    # For each node u:
    # If is_terminal[u] > 0:
    #   We must move these is_terminal[u] IDs to descendants.
    #   The cost is at least is_terminal[u] * 1 (if we move them to children).
    #   But we might need to move them further.
    
    # Let's simplify:
    # Every original ID must end up at a leaf in the final Trie.
    # Let's say we have the original Trie.
    # For each node u, let S(u) be the number of original IDs in its subtree.
    # If we are at node u, and we have S(u) IDs to place in its subtree.
    # If u is a leaf in the original Trie, S(u) = is_terminal[u].
    # All these S(u) IDs must be moved to some leaves.
    # But wait, the "leaves" are not fixed. We can create new leaves.
    # The cost to move an ID from u to a child is 1.
    # If we move all S(u) IDs from u to its children, the
