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
    # and a flag indicating if it's an end-of-string node.
    # Using lists for speed in Python.
    # trie[u] = [child0, child1, is_end]
    trie = [[-1, -1, 0]]
    
    for _ in range(n):
        s = sys.stdin.readline().strip()
        u = 0
        for char in s:
            bit = int(char)
            if trie[u][bit] == -1:
                trie[u][bit] = len(trie)
                trie.append([-1, -1, 0])
            u = trie[u][bit]
        trie[u][2] += 1 # Count how many strings end here

    # The problem asks for the minimum bits to add so that no string is a prefix of another.
    # This is equivalent to making every original string end at a leaf in the Trie.
    # However, we can't just make them leaves; we must ensure that if we extend a string,
    # the new string doesn't become a prefix of another.
    # Actually, the condition "no cow can ever be mistaken for another" means 
    # the set of final IDs must be prefix-free.
    # In a Trie, a set of strings is prefix-free if no end-of-string node is an ancestor of another.
    # To achieve this with minimum cost, for every node that is an end-of-string, 
    # if it has descendants, we must extend it.
    # But wait, the problem says we can append bits to *each* original ID.
    # If we have '01' and '011', '01' is a prefix of '011'. We must extend '01' to something 
    # that is not a prefix of '011' and '011' is not a prefix of it.
    # The most efficient way to make a set of strings prefix-free is to ensure 
    # every string ends at a leaf in a Trie where no end-of-string node is an ancestor of another.
    
    # Let's re-evaluate: We want to pick a set of nodes in the Trie such that:
    # 1. Every original string's path passes through exactly one chosen node.
    # 2. No chosen node is an ancestor of another chosen node.
    # 3. The sum of (depth(chosen_node) - depth(original_string_node)) is minimized.
    # Wait, the rule is: "If a reported prefix is the full final ID of a different cow, theft occurs."
    # This means if cow A's ID is '01' and cow B's ID is '011', if B reports '01', theft.
    # So no ID can be a prefix of another.
    
    # This is equivalent to: for every node u that is an end-of-string, 
    # if there are any strings in its subtree, we must move the end-of-string marker 
    # of u to some descendant node such that the new node is a leaf (or at least 
    # doesn't have other end-of-strings in its subtree).
    # Actually, the simplest way to think about it:
    # We want to select N nodes in the Trie such that no node is an ancestor of another,
    # and each original string's end-node is an ancestor of (or equal to) its selected node.
    # To minimize cost, we want to pick nodes as close to the original end-nodes as possible.
    
    # Let dp[u] be the minimum cost to satisfy the condition for all strings ending in subtree u.
    # If u is an end-of-string node (count > 0):
    # We MUST move these strings to leaves. But we can't just move them to any leaf.
    # If we move a string from u to a descendant, it costs (depth_descendant - depth_u).
    # However, we can only move them to nodes that are not ancestors of other strings.
    
    # Correct approach:
    # For each node u, let f(u) be the number of strings that "must" be satisfied in its subtree.
    # If u is an end-of-string, we have `trie[u][2]` strings that must be moved to leaves.
    # If u is not an end-of-string, we just pass up the strings from its children.
    # But we can only "use" a leaf to satisfy a string.
    # This is actually a greedy problem on the Trie.
    # For each node u, we calculate how many "available" leaf slots are in its subtree.
    # A leaf slot is a path that doesn't contain any end-of-string nodes.
    # But we can create new leaves by extending.
    
    # Let's use the property: To make N strings prefix-free, we need N leaves in a Trie.
    # Each original string $i$ ends at node $v_i$. We need to pick $N$ nodes $w_i$ such that
    # $w_i$ is in the subtree of $v_i$, and no $w_i$ is an ancestor of $w_j$.
    # The cost is $\sum (depth(w_i) - depth(v_i))$.
    # This is equivalent to $\sum depth(w_i) - \sum depth(v_i)$.
    # To minimize $\sum depth(w_i)$, we should pick the $N$ nodes with smallest depths 
    # that satisfy the prefix-free property and the subtree property.
    
    # Actually, the problem is simpler:
    # For each node u, let `count[u]` be the number of original strings ending at `u`.
    # We need to find $N$ nodes such that no node is an ancestor of another, 
    # and for each $u$, we pick at least `count[u]` nodes in its subtree.
    # Wait, that's not right. Each string is unique.
    # Let's use the "available leaves" idea.
    # For a node $u$, let $S(u)$ be the number of strings that end in the subtree of $u$.
    # Let $L(u)$ be the maximum number of prefix-free nodes we can pick in the subtree of $u$.
    # If $u$ is a leaf in the Trie, $L(u) = 1$ if $count[u] > 0$ else $0$.
    # This is not quite right because we can extend strings.
    
    # Let's use the greedy approach:
    # For each node $u$, we want to know how many strings are "passing through" $u$ 
    # that haven't been assigned to a leaf yet.
    # If $u$ is an end-of-string, those strings MUST be moved to leaves.
    # If we move a string from $u$ to a leaf in its subtree, it costs (depth_leaf - depth_u).
    # Total cost = $\sum_{i=1}^N (depth(w_i) - depth(v_i))$.
    # This is $\sum depth(w_i) - \sum depth(v_i)$.
    # We need to pick $N$ nodes $w_i$ such that they are prefix-free and $w_i$ is in subtree of $v_i$.
    # This is equivalent to:
    # For each node $u$, let $c(u)$ be the number of strings ending at $u$.
    # We need to pick $N$ nodes. Let $x(u)$ be the number of picked nodes in subtree $u$.
    # 1. $x(u) \le \text{number of children of } u \text{ (if we don't pick } u \text{ itself)}$
    # 2. If we pick $u$, $x(u) = 1$.
    # 3. $x(u) = \sum_{v \in children(u)} x(v)$ if we don't pick $u$.
    # 4. $x(u) \ge c(u)$ is not quite right.
    
    # Let's re-read: "You may append bits to the end of each original ID."
    # This means we can turn '01' into '010' or '011'.
    # If we have '01' and '011', we can turn '01' into '010'.
    # Now we have '010' and '011'. They are prefix-free.
    # Total cost: 1 bit.
    
    # Correct Greedy:
    # For each node $u$ in the Trie, let $f(u)$ be the number of strings that end at $u$.
    # We want to move these $f(u)$ strings to leaves in the subtree of $u$ such that 
    # they don't conflict with strings in other subtrees.
    # Let $g(u)$ be the number of "available" leaf slots in the subtree of $u$.
    # If $u$ is a leaf in the Trie:
    #   $g(u) = 1$ if $f(u) > 0$ else $0$.
    #   Wait, if $f(u) > 0$, we have $f(u)$ strings. We can only pick $u$ as a leaf once.
    #   If $f(u) > 1$, we MUST extend the extra $f(u)-1$ strings.
    #   But the problem says "each cow has a bitstring ID". The IDs are distinct?
    #   "If a reported prefix is the full final ID of a different cow..."
    #   This implies the final IDs must be distinct.
    #   If two cows have the same original ID, we must extend one of them.
    #   But the constraints say "Every ID is non-empty" and "N cows". 
    #
