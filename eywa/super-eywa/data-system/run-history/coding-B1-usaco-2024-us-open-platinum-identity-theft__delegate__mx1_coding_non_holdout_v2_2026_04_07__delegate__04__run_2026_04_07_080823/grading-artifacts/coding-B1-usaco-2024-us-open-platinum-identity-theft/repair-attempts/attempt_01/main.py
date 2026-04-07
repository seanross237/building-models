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
    # is_end stores the count of original IDs ending at this node
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

    # The problem asks for the minimum bits to append so no ID is a prefix of another.
    # If ID A is a prefix of ID B, we MUST append bits to A to make it not a prefix.
    # However, the problem says "If a reported prefix is the full final ID of a different cow, 
    # Bessie thinks identity theft happened."
    # This means if A is a prefix of B, B's reported prefix (A) matches A's full ID.
    # To prevent this, for every node in the Trie that is a terminal node (is_end > 0),
    # we must ensure that no other cow's ID is in its subtree.
    # But we can only append bits to the IDs. 
    # If we append bits to ID A, it becomes longer. If A was a prefix of B, 
    # making A longer might make it no longer a prefix of B.
    # Wait, the rule is: "If a reported prefix is the full final ID of a different cow".
    # If cow B reports prefix P, and P == ID of cow A, theft occurs.
    # To prevent this, for every cow B, all its possible prefixes (including itself) 
    # must not be the full ID of any other cow A.
    # This means no ID can be a prefix of another ID.
    # If ID A is a prefix of ID B, we must append bits to A to make it not a prefix of B.
    # But appending to A makes it longer, so it might still be a prefix of B.
    # Actually, the only way to stop A being a prefix of B is to make A longer 
    # than B, or make B longer such that A is no longer a prefix? No, that's impossible.
    # If A is a prefix of B, A will always be a prefix of B unless we change A.
    # If we append bits to A, A becomes A'. If A' is still a prefix of B, theft still happens.
    # If A' is no longer a prefix of B, theft is prevented.
    # BUT, the problem says "no cow can ever be mistaken for another".
    # This means for any cow i, no prefix of its ID can be the full ID of cow j (i != j).
    # This is exactly the condition: No ID is a prefix of another ID.
    # If A is a prefix of B, we must append bits to A such that A is no longer a prefix of B.
    # This is impossible by only appending to A (A will always be a prefix of B if len(A) < len(B)).
    # Wait, the only way is to append bits to B? No, if we append to B, A is still a prefix.
    # Let's re-read: "If a reported prefix is the full final ID of a different cow, Bessie thinks identity theft happened."
    # If cow B reports prefix P, and P == ID of cow A, theft.
    # To prevent this, for every cow B, all its prefixes must not be the full ID of any other cow A.
    # This means for every cow B, no prefix of B (including B itself) can be the ID of another cow A.
    # This is equivalent to: No ID is a prefix of another ID.
    # If A is a prefix of B, we must append bits to A to make it NOT a prefix of B.
    # But appending to A makes it longer. If A is a prefix of B, and we append 'x' to A,
    # A+x is a prefix of B only if B starts with A+x.
    # If we want to make A not a prefix of B, we must make A longer than B.
    # But the problem says "no cow can ever be mistaken for another".
    # This means for any cow i, and any prefix P of ID_i, P != ID_j for all j != i.
    # This is exactly: No ID is a prefix of another ID.
    # If A is a prefix of B, we must append bits to A to make it not a prefix of B.
    # This is only possible if we make A longer than B.
    # But if we make A longer than B, A is no longer a prefix of B.
    # However, B might now be a prefix of A!
    # The condition "no cow can ever be mistaken for another" means:
    # For all i, j (i != j), ID_i is not a prefix of ID_j AND ID_j is not a prefix of ID_i.
    # This is the definition of a Prefix Code (like Huffman).
    # In a Trie, this means no terminal node is an ancestor of another terminal node.
    # If a node is terminal, it cannot have any descendants that are terminal.
    # If a node is terminal and has descendants, we must "push" the descendants 
    # or "push" the terminal node. But we can only append bits.
    # Appending bits to a node moves it deeper in the Trie.
    # If node U is terminal and has descendants that are terminal, we must append bits to U
    # to move it to a position where it's not an ancestor of those descendants.
    # To minimize bits, for each terminal node, we want to move it to the nearest 
    # available leaf position that doesn't violate the prefix property.
    # Actually, the problem is: we have a set of strings. We want to add minimum bits 
    # such that no string is a prefix of another.
    # This is equivalent to: in the Trie, every terminal node must be a leaf.
    # If a terminal node has children, we must move the terminal node deeper.
    # But we can't move it "sideways", only deeper.
    # If we move a terminal node deeper, it might become a prefix of its former descendants.
    # The correct approach: For each node in the Trie, if it's a terminal node, 
    # it "consumes" that path. Any other terminal nodes in its subtree must be 
    # moved to other branches.
    # Wait, the problem is simpler: We want to select a set of nodes in the Trie 
    # such that no selected node is an ancestor of another, and all original 
    # strings are represented by these nodes.
    # But we can only append bits. This means we can only move a string to a descendant node.
    # If string A is a prefix of string B, we must append bits to A to make it 
    # a descendant of B, or append bits to B to make it a descendant of A? No.
    # If A is a prefix of B, we must append bits to A so that A is no longer a prefix of B.
    # This means A must become a descendant of B.
    # If A is a prefix of B, we must append bits to A to make it a descendant of B.
    # The number of bits to append to A to make it a descendant of B is (len(B) - len(A)) + 1?
    # No, if we make A a descendant of B, then B is a prefix of A. Still theft!
    # The only way is to make A and B such that neither is a prefix of the other.
    # This means they must diverge at some node.
    # If A is a prefix of B, they already share a path. To make them diverge, 
    # we must append bits to A to make it "branch off" from the path to B.
    # For example, if A="0" and B="01", we can change A to "00". 
    # Now A is no longer a prefix of B, and B is no longer a prefix of A.
    # Cost: 1 bit.
    # In the Trie, if a node is terminal and has descendants, we must move the terminal 
    # node to a different branch.
    # For each terminal node, if it has descendants, we must move it to a child 
    # that is NOT on the path to any other terminal node.
    # But we want to minimize total bits.
    # This is a greedy approach on the Trie:
    # For each node, calculate how many terminal nodes are in its subtree.
    # If a node is terminal, it must be "moved" to a leaf.
    # Actually, the problem is: we want to pick N nodes in the Trie such that 
    # no node is an ancestor of another, and each original string is a prefix of 
    # exactly one picked node.
    # Let's use the property: for each node, we want to know how many terminal 
    # nodes are in its subtree.
    # If a node is terminal, it must be moved to a leaf.
    # The cost to move a terminal node from depth `d` to depth `D` is `D - d`.
    # This is not quite right. Let's re-read again.
    # "You may append bits to the end of each original ID."
    # If A is a prefix of B, we can append bits to A to make it not a prefix of B.
    # To make A not a prefix of B, A must diverge from B at some point.
    # The earliest they can diverge is at some node on the path to B.
    # If A is a prefix of B, A is at some node `u`. B is at some descendant `v`.
    # We must append bits to A to move it to a child of `u` that is not on the path to `v`.
    #
