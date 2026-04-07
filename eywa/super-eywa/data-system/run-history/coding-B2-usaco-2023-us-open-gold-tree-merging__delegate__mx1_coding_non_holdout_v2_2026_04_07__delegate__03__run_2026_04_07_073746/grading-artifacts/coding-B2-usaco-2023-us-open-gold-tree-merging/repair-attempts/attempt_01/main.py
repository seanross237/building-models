import sys

# Increase recursion depth for deep trees
sys.setrecursionlimit(2000)

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    idx = 0
    T_cases = int(input_data[idx])
    idx += 1
    
    for _ in range(T_cases):
        N = int(input_data[idx])
        idx += 1
        
        adj_init = [[] for _ in range(N + 1)]
        parent_init = [0] * (N + 1)
        for _ in range(N - 1):
            u = int(input_data[idx])
            v = int(input_data[idx+1])
            idx += 2
            # The problem says "v p" describing an edge. 
            # Usually in tree problems, p is parent of v.
            # Let's assume v is child, p is parent.
            adj_init[v].append(u) # This is wrong based on "v p" description.
            # Re-reading: "v p" describing an edge. 
            # In USACO, usually it's child parent or parent child.
            # Let's assume the second value is the parent.
            # Wait, the problem says "v p" describing an edge. 
            # Let's assume p is parent of v.
            pass 
        
        # Re-parsing logic:
        # The input format "v p" is slightly ambiguous. 
        # Let's assume the second value is the parent of the first.
        # Let's re-read: "v p" describing an edge.
        # Let's try: p is parent of v.
        
        # Resetting idx for the actual logic
        idx -= (N-1)*2
        
        adj_init = [[] for _ in range(N + 1)]
        parent_init = [0] * (N + 1)
        for _ in range(N - 1):
            v = int(input_data[idx])
            p = int(input_data[idx+1])
            idx += 2
            adj_init[p].append(v)
            parent_init[v] = p
            
        M = int(input_data[idx])
        idx += 1
        adj_final = [[] for _ in range(N + 1)]
        parent_final = [0] * (N + 1)
        for _ in range(M - 1):
            v = int(input_data[idx])
            p = int(input_data[idx+1])
            idx += 2
            adj_final[p].append(v)
            parent_final[v] = p

        # The problem asks for a sequence of merges.
        # A merge of siblings u and v (u < v) results in v.
        # This means in the final tree, a node v is the result of merging 
        # some set of siblings from the initial tree.
        # All nodes in that set must have the same parent in the initial tree.
        # Also, the children of v in the final tree must be the union of children 
        # of all nodes in that set in the initial tree.
        
        # To find the merges:
        # For each node in the final tree, identify which nodes in the initial tree 
        # were merged to form it.
        # Since it's guaranteed a solution exists, we can work bottom-up or top-down.
        # A node 'u' in the final tree is formed by a set of nodes {s1, s2, ...} 
        # in the initial tree such that max(s1, s2, ...) = u.
        
        # Let's find for each node in the final tree, which initial nodes it "represents".
        # Because the merge operation preserves the larger value, 
        # if node 'u' is in the final tree, it must have existed in the initial tree.
        # Any other node 'v' that was merged into 'u' must have v < u and parent(v) == parent(u).
        
        merges = []
        
        # We can find the merges by looking at the siblings in the initial tree.
        # For each parent in the initial tree, look at its children.
        # Some children might be merged into a single child in the final tree.
        
        # Let's map each initial node to its final representative.
        # Since the problem guarantees a solution, we can find which initial nodes 
        # belong to which final node.
        # A node 'u' in the initial tree belongs to final node 'f' if 
        # 'f' is an ancestor of 'u' in the final tree and 'u' is an ancestor of 'f' is not possible.
        # Actually, if 'u' is merged into 'f', then 'f' is the max value in the set.
        
        # Let's use the property: if u and v are siblings in the initial tree and 
        # they are merged, they must have the same parent.
        # The final tree is a "compressed" version of the initial tree.
        
        # For each node in the initial tree, find its "target" node in the final tree.
        # We can do this by traversing from the root of the initial tree.
        # But the roots might be different. However, the problem says "rooted tree".
        # The root of the initial tree must be the same as the root of the final tree?
        # Not necessarily, but the merge operation only affects siblings.
        # So the root of the initial tree must be the root of the final tree.
        
        root_init = 1
        for i in range(1, N + 1):
            if parent_init[i] == 0:
                root_init = i
                break
        
        root_final = 1
        for i in range(1, N + 1):
            if parent_final[i] == 0:
                root_final = i
                break
                
        # To find merges:
        # For each node in the final tree, its children are a subset of the 
        # children of the nodes that were merged to form it.
        # Let's find for each node in the initial tree, which node in the final tree it belongs to.
        # We can use a DFS on the initial tree.
        
        target = [0] * (N + 1)
        
        def find_targets(u_init, u_final):
            target[u_init] = u_final
            # The children of u_final in the final tree are formed by 
            # merging some children of u_init.
            # Let's group children of u_init by which child of u_final they belong to.
            
            # Map final_child -> list of initial_children
            groups = {}
            # We need to know which initial_child belongs to which final_child.
            # We can find this by looking at the final tree structure.
            # But we don't know which initial_child is which final_child yet.
            # However, we know that if initial_child 'c' is merged into final_child 'fc',
            # then 'fc' must be a descendant of 'c' in the initial tree? No.
            # 'fc' is one of the initial children.
            
            # Let's use the property: if 'c' is an initial child of 'u_init',
            # and 'c' is merged into 'fc', then 'fc' is also a child of 'u_init' 
            # (or 'fc' is 'c' itself) and 'fc' is a child of 'u_final'.
            
            # Let's find which initial children of u_init are descendants of which final children of u_final.
            # This is still circular. Let's simplify.
            # For each node u in the initial tree, it is either a node in the final tree
            # or it is merged into some sibling.
            pass

        # Correct approach:
        # For each node u in the initial tree, if it's not in the final tree, 
        # it must be merged with a sibling.
        # Which sibling? The one that is its "representative" in the final tree.
        # A node u is in the final tree if it appears as a node in the final tree.
        # Let's identify all nodes that are in the final tree.
        is_in_final = [False] * (N + 1)
        for i in range(1, N + 1):
            if parent_final[i] != 0 or i == root_final:
                # This is not enough. A node is in the final tree if it's a node in the final tree.
                # The input gives M nodes in the final tree.
                pass
        
        # Let's re-read: "The final tree uses values drawn from the same set [1..N]".
        # The final tree has M nodes.
        # Let's collect all nodes present in the final tree.
        final_nodes = set()
        for i in range(1, N + 1):
            # A node is in the final tree if it's the root or has a parent in the final tree.
            # But we only know the edges. Let's find all nodes mentioned in the final tree edges.
            pass
        
        # Let's use the edges to find all nodes in the final tree.
        # The input for final tree is M-1 edges.
        # The nodes are from the set 1..N.
        # A node is in the final tree if it's part of an edge or it's the root.
        # Wait, the number of nodes in the final tree is M.
        # Let's find the M nodes.
        
        # Let's re-parse the final tree edges properly.
        # The input for final tree is M-1 lines of "v p".
        # This means there are M nodes.
        # Let's find them.
        
        # Actually, the simplest way to find merges:
        # For each node u in the initial tree, if u is not in the final tree,
        # it must be merged with
