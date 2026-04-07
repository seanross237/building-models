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
        has_parent_init = [False] * (N + 1)
        for _ in range(N - 1):
            u = int(input_data[idx])
            v = int(input_data[idx+1])
            idx += 2
            # The problem says "v p" describing an edge. 
            # Usually, this means v is child, p is parent.
            # Let's assume v is child, p is parent based on "v p".
            # Wait, the problem says "v p" describing an edge. 
            # Let's check standard USACO format. Usually it's child parent.
            # Let's treat the second value as parent.
            child, parent = u, v
            adj_init[parent].append(child)
            has_parent_init[child] = True
            
        root_init = 1
        for i in range(1, N + 1):
            if not has_parent_init[i]:
                root_init = i
                break
                
        M = int(input_data[idx])
        idx += 1
        adj_final = [[] for _ in range(N + 1)]
        has_parent_final = [False] * (N + 1)
        for _ in range(M - 1):
            u = int(input_data[idx])
            v = int(input_data[idx+1])
            idx += 2
            child, parent = u, v
            adj_final[parent].append(child)
            has_parent_final[child] = True
            
        root_final = 1
        for i in range(1, N + 1):
            if not has_parent_final[i]:
                root_final = i
                break

        # To solve this, we need to find which children of a node in the initial tree
        # merge into which children of the corresponding node in the final tree.
        # Since a merge keeps the larger value, a child in the final tree must be 
        # the maximum value among the set of initial nodes that merge into it.
        
        merges = []

        def get_merges(u_init, u_final):
            # u_init is the current node in the initial tree
            # u_final is the current node in the final tree
            
            # Children in final tree
            f_children = adj_final[u_final]
            # Children in initial tree
            i_children = adj_init[u_init]
            
            # We need to partition i_children into groups, where each group 
            # merges into one f_child.
            # A child 'c' in i_children belongs to f_child if f_child is 
            # an ancestor of 'c' in the final tree? No, that's not right.
            # The problem says: "The merged node keeps the larger value... 
            # and its children become the union of both child sets."
            # This means if we merge siblings A and B, the new node is max(A, B).
            # The children of the new node are children(A) U children(B).
            
            # Let's map each initial child to its "target" final child.
            # Since the final tree is a subset of the initial tree's structure 
            # (in terms of ancestor-descendant relationships), 
            # each initial child 'c' must eventually be part of some final child 'fc'.
            # Because the final tree is formed by merging siblings, 
            # 'fc' must be a descendant of 'c' or 'c' itself.
            # Actually, 'c' must be an ancestor of 'fc' or 'c' == 'fc'.
            # Wait, the rule is: merge two siblings. This means the parent stays the same.
            # So if we merge siblings, the parent is the same.
            # Thus, all nodes that merge into 'fc' must be siblings in the initial tree.
            
            # Correct logic:
            # For a node u_init, its children in the initial tree are i_children.
            # Some of these i_children will be merged to form the children in the final tree.
            # Each child in the final tree (f_child) must be one of the i_children 
            # (specifically, the one with the maximum value in that merge group).
            
            # Let's find which i_child corresponds to which f_child.
            # Since the final tree is a result of merging siblings, 
            # for a node u_init, its children in the final tree are a subset of 
            # its children in the initial tree, but some initial children might 
            # have been merged.
            
            # Actually, the problem says "The merged node keeps the larger value".
            # This means if we merge siblings 3 and 5, the new node is 5.
            # The children of 5 are the union of children of 3 and 5.
            # This implies that the final tree's nodes are a subset of the initial tree's nodes.
            # And for any node in the final tree, its children are a subset of the 
            # union of children of the nodes that merged to form it.
            
            # Let's use the property: every node in the final tree exists in the initial tree.
            # For each node u in the final tree, its children in the final tree 
            # are a subset of the children of the nodes that merged to form u.
            
            # Let's track which initial node corresponds to which final node.
            # Since the final tree is a "compressed" version, each final node 
            # is exactly one of the initial nodes.
            
            # Let's find for each initial node, which final node it "becomes".
            # But the problem says "The merged node keeps the larger value".
            # This means if we merge 3 and 5, the node 5 remains.
            # So every node in the final tree is an original node.
            
            # For each node u in the initial tree, if it's not in the final tree,
            # it must be merged with a sibling that has a larger value.
            
            # Let's find which nodes are "kept" (are in the final tree).
            is_in_final = [False] * (N + 1)
            for i in range(1, N + 1):
                # A node is in the final tree if it's the root or has a parent in the final tree.
                # Wait, the final tree has M nodes.
                pass # We'll use the has_parent_final logic.
            
            # Actually, the simplest way:
            # For each node u in the initial tree, if it has a parent p in the initial tree,
            # but u is not a child of p in the final tree, then u must be merged 
            # with some sibling.
            
            # Let's refine:
            # For each parent p in the initial tree:
            #   The children of p in the final tree are a subset of the children of p in the initial tree.
            #   Wait, that's not necessarily true. A child in the final tree could be 
            #   the result of merging several children in the initial tree.
            #   BUT, the rule says "The merged node keeps the larger value".
            #   So if we merge siblings 3 and 5, the result is 5. 
            #   The children of 5 are the union of children of 3 and 5.
            #   This means the node 5 is still 5.
            #   So the set of nodes in the final tree is a subset of the initial nodes.
            #   And for any node u in the final tree, its children in the final tree 
            #   are a subset of the children of the nodes that merged to form u.
            #   Wait, if we merge 3 and 5 to get 5, the children of 5 in the final tree 
            #   could be children of 3 OR children of 5.
            
            # Let's re-read: "The merged node keeps the larger value... and its children 
            # become the union of both child sets."
            # This means if we merge siblings A and B (A < B), the new node is B.
            # The children of B are now children(A) + children(B).
            # This is exactly what happens in a tree where we "absorb" A into B.
            
            # So, for each node u in the initial tree, if u is not in the final tree,
            # it must be merged with a sibling v such that v > u.
            # Which sibling? The one that "eventually" becomes the node in the final tree.
            
            # Let's identify for each node u in the initial tree, which node in the 
            # final tree it belongs to.
            # A node u in the initial tree belongs to node v in the final tree if 
            # v is the smallest ancestor of u (including u) that is in the final tree.
            # No, that's not right. The merge is between siblings.
            # If u is merged with sibling v, they must have the same parent.
            
            # Let's use this:
            # For each parent p in the initial tree:
            #   The children of p in the initial tree are {c1, c2, ..., ck}.
            #   The children of p in the final tree are {fc1, fc2, ..., fcm}.
            #   Each fc_j must be one of the ci.
            #   And each ci must either be some fc_j or be merged into some fc_j.
            #   Since the merge keeps the larger value, if ci is merged into fc_j,
