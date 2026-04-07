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
    # trie[node] = [child0, child1, is_end_of_id]
    # Using lists for speed in Python
    trie = [[-1, -1, False]]
    
    for s in ids:
        curr = 0
        for char in s:
            bit = 0 if char == '0' else 1
            if trie[curr][bit] == -1:
                trie[curr][bit] = len(trie)
                trie.append([-1, -1, False])
            curr = trie[curr][bit]
        trie[curr][2] = True

    # The problem asks for the minimum bits to append so no ID is a prefix of another.
    # This is equivalent to: in the Trie, no node marked 'is_end_of_id' can be an 
    # ancestor of another node marked 'is_end_of_id'.
    # However, the problem says: "If a reported prefix is the full final ID of a different cow..."
    # This means if cow A's ID is a prefix of cow B's ID, B can report a prefix that is A's ID.
    # To prevent this, we must append bits to IDs such that no ID is a prefix of another.
    
    # Let's re-read: "If a reported prefix is the full final ID of a different cow, Bessie thinks identity theft happened."
    # If cow A has ID "01" and cow B has ID "011", B can report "01", which is A's ID.
    # We need to append bits to IDs so that no ID is a prefix of another.
    
    # In a Trie, if a node is marked as an ID, no descendant can be an ID.
    # If we have a node that is an ID and it has descendants that are also IDs,
    # we must "push" the ID node down by appending bits.
    
    # Actually, the problem is simpler: 
    # We want to select a set of nodes in the Trie such that:
    # 1. Every original ID is an ancestor of (or is) one of the selected nodes.
    # 2. No selected node is an ancestor of another selected node.
    # 3. The sum of (depth of selected node - depth of original ID node) is minimized.
    
    # Wait, the rule is: "no cow can ever be mistaken for another".
    # This means for any two cows A and B, A's ID cannot be a prefix of B's ID.
    # This is exactly the condition that no ID is a prefix of another.
    
    # Let's use DP on the Trie.
    # For a node u:
    # If u is an end-of-ID node:
    #    We must either:
    #    1. Keep it as is, but then no descendant can be an end-of-ID.
    #       But we MUST satisfy all original IDs. If there are IDs in the subtree,
    #       we must push this ID node down to a leaf or a position where it's not a prefix.
    #       Actually, the rule is: we can append bits to the *original* IDs.
    #       If we append bits to ID '01' to make it '010', it's no longer a prefix of '011'.
    
    # Correct approach:
    # For each node in the Trie, we want to know how many "ID-ends" are in its subtree.
    # If a node is an end-of-ID, it "occupies" that position. 
    # If there are other IDs in its subtree, we must push this ID down.
    # But we can only push it down to a branch that is NOT used by another ID.
    
    # Let's refine:
    # Each original ID must end at some node in the Trie.
    # Let $S$ be the set of nodes where the $N$ IDs end.
    # We want to find a set of nodes $S'$ such that:
    # 1. For every $u \in S$, there is a $v \in S'$ such that $u$ is an ancestor of $v$.
    # 2. No $v_1, v_2 \in S'$ have an ancestor-descendant relationship.
    # 3. $\sum_{v \in S'} (depth(v) - depth(u_{corresponding})) \to$ this is not quite right because 
    #    one $v$ could potentially cover multiple $u$'s? No, each cow is distinct.
    #    Each cow $i$ starts at $u_i$ and ends at $v_i$. $v_i$ must be in the subtree of $u_i$.
    #    The cost is $\sum (depth(v_i) - depth(u_i))$.
    #    Constraint: No $v_i$ is an ancestor of $v_j$.
    
    # This is equivalent to:
    # In the Trie, we need to pick $N$ nodes such that no node is an ancestor of another,
    # and each original ID node has one of these picked nodes in its subtree.
    # To minimize $\sum depth(v_i)$, we should pick nodes as high as possible.
    
    # Let's use the property: To satisfy $N$ IDs, we need $N$ leaves in a pruned version of the Trie.
    # A node can be a "leaf" if it's not an ancestor of another "leaf".
    # If a node $u$ is an end-of-ID, it must have a leaf in its subtree.
    # If $u$ is an end-of-ID and we pick $u$ itself, cost is 0. But we can only do this if 
    # no other $v$ is in $u$'s subtree.
    
    # Let $f(u)$ be the minimum cost to satisfy all end-of-ID nodes in the subtree of $u$.
    # If $u$ is an end-of-ID:
    #    We must pick a node in $u$'s subtree to represent this ID.
    #    If we pick $u$, cost is 0, but we can't pick any other node in $u$'s subtree.
    #    This is only possible if there are no other end-of-ID nodes in $u$'s subtree.
    #    Wait, the problem says "no cow can ever be mistaken for another".
    #    This means the final IDs must be prefix-free.
    #    If we have two cows with original IDs "0" and "00", we must change "0" to "01" (or something)
    #    so that "0" is not a prefix of "00".
    
    # Let's use the "available slots" idea.
    # Each node in the Trie can provide at most 2 children (slots).
    # A node $u$ that is an end-of-ID needs to be "pushed" to a leaf.
    # If $u$ is an end-of-ID, it needs 1 slot.
    # If $u$ is not an end-of-ID, it can pass up the number of slots needed by its children.
    
    # Let $dp[u]$ = minimum cost to satisfy all end-of-ID nodes in subtree of $u$.
    # This is still slightly wrong. Let's use the "greedy" approach for prefix-free sets.
    # To have $K$ prefix-free strings in a subtree, we need to use the available branches.
    
    # Let $count[u]$ be the number of end-of-ID nodes in the subtree of $u$.
    # If $u$ is an end-of-ID, it's one of the $count[u]$ nodes.
    # The number of "available" leaf positions in the subtree of $u$ is at most 
    # the number of leaves in the Trie.
    
    # Let's use the following:
    # For each node $u$, let $needed[u]$ be the number of end-of-ID nodes in its subtree.
    # We want to assign each of these $needed[u]$ nodes to a unique leaf in the Trie.
    # To minimize cost, we want to assign them to leaves as close to their original nodes as possible.
    
    # Actually, the problem is:
    # We have $N$ nodes in the Trie. We want to move each node $u_i$ to a new node $v_i$ 
    # such that $v_i$ is in the subtree of $u_i$, and all $v_i$ are prefix-free.
    # This is equivalent to: $v_i$ are leaves in some subtree.
    # The minimum cost is $\sum (depth(v_i) - depth(u_i))$.
    
    # Let's use the property:
    # A node $u$ can "provide" its children to satisfy the requirements of its subtree.
    # If $u$ is an end-of-ID, it needs 1 slot.
    # If $u$ is not an end-of-ID, it can provide the sum of slots needed by its children.
    # But a node $u$ can only provide at most 2 slots (its children).
    # If $u$ is an end-of-ID, it *must* be satisfied. If we don't satisfy it at $u$, 
    # we must satisfy it at some descendant.
    
    # Let's re-read: "You may append bits to the end of each original ID."
    # This means we can only move an ID *down* its own subtree.
    # If we have "0" and "00", we can change "0" to "01".
    # "0" is at depth 1, "01" is at depth 2. Cost = 1.
    # "00" is at depth 2. It stays "0
