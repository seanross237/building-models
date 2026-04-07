import sys

# Increase recursion depth for deep Tries
sys.setrecursionlimit(2000000)

def solve():
    # Read N
    line = sys.stdin.readline()
    if not line:
        return
    n = int(line.strip())
    
    # Trie structure using lists for efficiency
    # trie[node] = [child0, child1, count_of_ends_at_this_node]
    # Using a single flat list to represent nodes to save memory/time
    # node structure: [left_child, right_child, end_count]
    trie = [[-1, -1, 0]]
    
    for _ in range(n):
        s = sys.stdin.readline().strip()
        curr = 0
        for char in s:
            bit = 0 if char == '0' else 1
            if trie[curr][bit] == -1:
                trie[curr][bit] = len(trie)
                trie.append([-1, -1, 0])
            curr = trie[curr][bit]
        trie[curr][2] += 1

    total_cost = 0

    # We need to ensure that for every node that is an end of an ID,
    # it is not a prefix of another ID. 
    # However, the problem says: "If a reported prefix is the full final ID of a different cow..."
    # This means if cow A's ID is a prefix of cow B's ID, we must extend A.
    # But we can extend ANY cow. The goal is to make sure no ID is a prefix of another.
    # Actually, the rule is: if cow A reports a prefix, and that prefix is cow B's full ID.
    # This happens if ID_B is a prefix of ID_A.
    # To prevent this, for every node that is an end-of-ID, it must not have any descendants 
    # that are also end-of-IDs. 
    # Wait, the rule is: "If a reported prefix is the full final ID of a different cow..."
    # If cow A has ID "01" and cow B has ID "011".
    # Cow B can report prefix "01". This is cow A's full ID. Identity theft!
    # So we must extend cow A so it's no longer "01".
    # But we can also extend cow B. 
    # Actually, the problem is: we want to add bits to IDs such that no ID is a prefix of another.
    # This is equivalent to saying in the Trie, no end-of-ID node is an ancestor of another end-of-ID node.
    
    # Let's refine: For every node in the Trie, if it's an end-of-ID, we must ensure 
    # it has