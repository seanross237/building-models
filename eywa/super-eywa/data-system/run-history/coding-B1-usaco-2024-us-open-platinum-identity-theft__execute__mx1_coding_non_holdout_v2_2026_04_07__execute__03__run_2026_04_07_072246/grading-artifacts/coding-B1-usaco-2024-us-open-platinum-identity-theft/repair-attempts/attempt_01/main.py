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

    # Trie structure using lists for speed in Python
    # trie[u][0] = child '0', trie[u][1] = child '1'
    # is_terminal[u] = number of original strings ending at node u
    # We use a single list for children to save memory: trie[u*2], trie[u*2+1]
    
    # Pre-calculate total length to estimate size
    # Max nodes = total length + 1
    max_nodes = sum(len(s) for s in ids) + 1
    trie = [-1] * (2 * max_nodes)
    is_terminal = [0] * max_nodes
    nodes_count = 1

    for s in ids:
        curr = 0
        for char in s:
            bit = int(char)
            idx = curr * 2 + bit
            if trie[idx] == -1:
                trie[idx] = nodes_count
                nodes_count += 1
            curr = trie[idx]
        is_terminal[curr] += 1

    # The problem: No string can be a prefix of another.
    # In the Trie, this means no terminal node can be an ancestor of another terminal node.
    # If a node is terminal, all its descendants must be "pushed" further down.
    # However, we can only append bits. This means if a node is terminal, 
    # we must ensure no other terminal node exists in its subtree.
    # But wait, the rule is: "If a reported prefix is the full final ID of a different cow..."
    # This means if Cow A's ID is P, and Cow B's ID is S, P cannot be a prefix of S.
    # This is exactly the prefix-free property.
    
    # To minimize bits added:
    # For every node that is a terminal node, we must ensure that no other 
    # terminal nodes exist in its subtree.
    # If a node is terminal, we can't "move" it. We must move its descendants.
    # But the problem says we can append bits to *each* original ID.
    # If ID_A is a prefix of ID_B, we must append bits to ID_A so it's no longer a prefix.
    # Or append bits to ID_B so it's no longer a descendant.
    # Actually, the most efficient way to resolve a terminal node having descendants 
    # is to treat the terminal node as a leaf and "redirect" the descendants 
    # to a new branch.
    
    # Let's re-read: "You may append bits to the end of each original ID."
    # If ID_A is a prefix of ID_B, we must append bits to ID_A to make it not a prefix.
    # Or append bits to ID_B to make it not a descendant.
    # Wait, if we append bits to ID_A, it becomes longer, so it might still be a prefix of ID_B.
    # If we append bits to ID_B, it becomes longer, so it's still a descendant.
    # The only way to stop ID_A being a prefix of ID_B is to make ID_A NOT a prefix.
    # This means ID_A must be extended until it is no longer a prefix of ID_B.
    # But if we extend ID_A, it might become ID_B!
    # The rule is: "If a reported prefix is the full final ID of a different cow..."
    # If Cow A's final ID is $S_A$ and Cow B's final ID is $S_B$, 
    # then $S_A$ cannot be a prefix of $S_B$.
    
    # This is equivalent to: In the Trie of final IDs, no terminal node is an ancestor of another.
    # We want to minimize total bits added.
    # For each node in the Trie, let's calculate how many terminal nodes are in its subtree.
    # If a node is terminal, it "blocks" its subtree.
    # To resolve this, we must move all terminal nodes in its subtree to be 
    # siblings of the current node or deeper.
    # Actually, the simplest way to think about it:
    # Every terminal node must be a leaf in the final Trie.
    # If a node is terminal and has descendants, we must extend the descendants 
    # or extend the terminal node.
    # But extending the terminal node is better if it's "cheaper".
    # Actually, the problem is: we have a set of strings. We want to add bits to 
    # make them prefix-free.
    # This is equivalent to: for every node in the Trie that is terminal, 
    # all its descendants must be moved to a different branch.
    # To minimize bits, for each terminal node, we look at its children.
    # If a child branch contains $k$ terminal nodes, we must move them.
    # The cost to move a terminal node from depth $d$ to a new branch at depth $d+1$ 
    # is not quite right.
    
    # Correct approach:
    # For each node $u$, let $f(u)$ be the minimum bits to add to all terminal nodes 
    # in the subtree of $u$ such that they are prefix-free and none is a prefix of $u$.
    # If $u$ is terminal, we must move all descendants to be "outside" $u$.
    # The best way to move a descendant is to make it a sibling of $u$ or a sibling 
    # of one of $u$'s ancestors.
    # Actually, the problem is simpler:
    # For each node $u$, if it is terminal, we must "remove" all terminal nodes 
    # in its subtree by appending bits to them.
    # To minimize bits, for each terminal node in the subtree, we want to 
    # append the minimum number of bits to make it not a descendant of $u$.
    # The minimum bits to make a descendant of $u$ not a descendant of $u$ 
    # is to append bits until it branches off.
    # But we can only append bits to the *original* IDs.
    # If we have a terminal node at depth $d$, and its ancestor is terminal at depth $d_{anc}$,
    # we must append bits to the descendant to make it not a descendant.
    # The minimum bits to add to a descendant at depth $d$ to make it not a descendant 
    # of an ancestor at depth $d_{anc}$ is to make it branch off at some depth $k \ge d_{anc}$.
    # Wait, if we append bits to the descendant, its depth increases.
    # If we append bits to the ancestor, its depth increases.
    # If we append bits to the ancestor, it might still be a prefix of the descendant.
    # The only way to make $S_{anc}$ not a prefix of $S_{desc}$ is to make $S_{anc}$ 
    # have a different bit at some position $i \le \text{length}(S_{anc})$.
    # But we can only *append* bits. We cannot change existing bits.
    # So if $S_{anc}$ is a prefix of $S_{desc}$, the only way to fix it is to 
    # append bits to $S_{anc}$ until it is no longer a prefix of $S_{desc}$.
    # But if we append bits to $S_{anc}$, it will still be a prefix of $S_{desc}$ 
    # unless we append bits such that the new $S_{anc}$ is no longer a prefix.
    # This is only possible if the new $S_{anc}$ is longer than $S_{desc}$.
    # But if $S_{anc}$ becomes longer than $S_{desc}$, then $S_{desc}$ is a prefix of $S_{anc}$!
    # This is the same problem.
    # The only way to satisfy the condition is:
    # For any two cows $i, j$, $S_i$ is not a prefix of $S_j$ AND $S_j$ is not a prefix of $S_i$.
    # This means in the Trie, no terminal node is an ancestor of another.
    # If $S_{anc}$ is a prefix of $S_{desc}$, we MUST append bits to $S_{desc}$ 
    # such that it is no longer in the subtree of $S_{anc}$.
    # But we can only append bits, which only makes it *deeper* in the subtree.
    # Wait, the only way to make $S_{desc}$ not a descendant of $S_{anc}$ 
    # is to change $S_{anc}$? No, we can't change $S_{anc}$.
    # Let's re-read: "If a reported prefix is the full final ID of a different cow, Bessie thinks identity theft happened."
    # If Cow A reports prefix $P$, and $P$ is the full ID of Cow B, theft.
    # This means for any cow $i$, no prefix of its final ID $S_i$ can be the final ID of another cow $j$.
    # This means $S_j$ cannot be a prefix of $S_i$.
    # This must hold for all $i, j$.
    # So $S_j$ is not a prefix of $S_i$ for all $i \neq j$.
    # This is exactly the prefix-free property.
    # If $S_{anc}$ is a prefix of $S_{desc}$, we MUST append bits to $S_{desc}$ 
    # to make it not a descendant? No, that's impossible.
    # We MUST append bits to $S_{anc}$ to make it not a prefix of $S_{desc}$.
    # But appending bits to $S_{anc}$ only makes it longer, so it's still a prefix 
    # unless it becomes longer than $S_{desc}$.
    # If $S_{anc}$ becomes longer than $S_{desc}$, then $S_{desc}$ is a prefix of $S_{anc}$.
    # This is the same
