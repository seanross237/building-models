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
        
        # Initial tree
        adj_init = [[] for _ in range(N + 1)]
        parent_init = [0] * (N + 1)
        for _ in range(N - 1):
            u = int(input_data[idx])
            p = int(input_data[idx+1])
            idx += 2
            adj_init[p].append(u)
            parent_init[u] = p
            
        # Final tree
        M = int(input_data[idx])
        idx += 1
        adj_final = [[] for _ in range(N + 1)]
        parent_final = [0] * (N + 1)
        for _ in range(M - 1):
            u = int(input_data[idx])
            p = int(input_data[idx+1])
            idx += 2
            adj_final[p].append(u)
            parent_final[u] = p

        # The problem guarantees a valid sequence exists.
        # A merge operation combines siblings and keeps the larger value.
        # This means for any node in the final tree, its children are a subset 
        # of the children of the corresponding node in the initial tree, 
        # or rather, the final node is the result of merging several initial siblings.
        
        # To find the merges:
        # For every node in the final tree, its children must be formed by 
        # merging groups of siblings in the initial tree.
        # However, the rule is: merge two siblings, keep the larger.
        # This implies that for a node 'u' in the final tree, all its children 
        # in the final tree must have been children of some node in the initial tree.
        
        # Let's identify which initial nodes are "merged" into which final nodes.
        # Since the values are the same and the larger value is kept, 
        # a node 'v' in the final tree must be one of the nodes in the initial tree.
        # Specifically, if node 'v' exists in both, it's the "survivor" of its group.
        
        # We can find the merges by looking at the parents.
        # For every node 'u' in the initial tree, if its parent in the initial tree 
        # is different from its parent in the final tree, it must have been merged 
        # into its final parent.
        
        # Wait, the rule is: "merge two distinct sibling nodes".
        # This means we can only merge nodes that share the same parent.
        # If node 'u' is a child of 'p' in the initial tree, and 'u' is a child of 'p_final' 
        # in the final tree, then 'u' must have been merged with its siblings 
        # until the remaining sibling is 'u' and its new parent is 'p_final'.
        # But the problem says "merge two distinct sibling nodes". This implies 
        # the parent doesn't change during a merge, only the number of children.
        # The only way the parent changes is if the parent itself is merged.
        
        # Let's re-read: "The merged node keeps the larger value... its children become the union".
        # This means if we merge siblings A and B (A < B), B becomes the new node.
        # B's children are now children(A) + children(B).
        # This is exactly what happens when we want to combine children.
        
        # Correct logic:
        # For each node 'p' in the initial tree, its children in the final tree 
        # must be a subset of the children of 'p' in the initial tree, 
        # OR some children of 'p' were merged into 'p' itself? No, siblings.
        # If siblings A and B are merged, the parent remains the same.
        # The only way a node's parent changes is if the parent is merged into its own sibling.
        
        # Let's track the current parent of each node.
        current_parent = list(parent_init)
        # We need to merge siblings in the initial tree to match the final tree.
        # A merge (u, v) is valid if current_parent[u] == current_parent[v].
        # We want to reach a state where current_parent[u] == parent_final[u] for all u.
        
        # Since we can only merge siblings, we can only change the set of children 
        # of a parent. We cannot change the parent of a node unless that node 
        # is merged with a sibling that has a different parent? No, siblings 
        # MUST have the same parent.
        
        # Re-reading: "One operation may merge two distinct sibling nodes."
        # This means the parent of the merged node is the same as the parent of the two siblings.
        # If we merge A and B (siblings), the new node is max(A, B).
        # The parent of max(A, B) is the same as the parent of A and B.
        # So the parent of a node can NEVER change.
        # Wait, if the parent can never change, then parent_init[u] must equal parent_final[u] 
        # for all u that exist in the final tree.
        # But the final tree might have fewer nodes.
        # If node 'u' is in the final tree, its parent in the final tree must be 
        # the same as its parent in the initial tree.
        
        # Let's check the constraints and the guarantee.
        # "It is guaranteed that at least one valid sequence exists."
        # This implies that for every node 'u' in the final tree, parent_init[u] == parent_final[u].
        # The only difference is that in the final tree, some siblings are merged.
        
        merges = []
        # For each parent, identify which children are in the final tree.
        # Any child in the initial tree that is NOT in the final tree must have been merged.
        # Actually, any child in the initial tree that is not a child in the final tree 
        # must be merged into one of the children that IS in the final tree.
        
        # Let's group initial children by their parent.
        for p in range(1, N + 1):
            if not adj_init[p]:
                continue
            
            # Children of p in initial tree
            init_children = adj_init[p]
            # Children of p in final tree
            final_children = adj_final[p]
            
            # The final_children must be a subset of init_children.
            # Each child in init_children that is not in final_children must be merged 
            # into one of the children in final_children.
            # Which one? The rule is: "The merged node keeps the larger value".
            # If we merge u and v, the survivor is max(u, v).
            # So if we want to merge 'u' into 'v', we need v > u.
            
            # Let's use a set for fast lookup
            final_set = set(final_children)
            
            # To merge all non-final children into final children:
            # For each u in init_children but not in final_set:
            # We must merge u with some v in final_set such that v > u.
            # Or merge u with some other non-final child w, and eventually merge the result into a final child.
            
            # Let's collect all initial children.
            # We want to reduce init_children to final_children.
            # We can only merge two siblings.
            
            # Sort initial children descending to make merging easier?
            # If we have children [1, 2, 5] and final is [5].
            # Merge 1 and 2 -> 2. Then merge 2 and 5 -> 5.
            # If final is [2, 5], merge 1 and 2 -> 2.
            
            # Correct approach:
            # For each parent p:
            # 1. Identify children in init_children but not in final_set.
            # 2. For each such child 'u', we need to merge it with some sibling 'v' 
            #    such that the survivor of the merge is eventually one of the final_children.
            # 3. The simplest way: for each u not in final_set, find a sibling v 
            #    such that v > u. If no such v exists in the final_set, 
            #    it must be that u is part of a merge that results in a final_child.
            #    But the problem says the survivor is the larger value.
            #    So if 'u' is not in the final tree, it MUST be smaller than the 
            #    node it is merged into.
            
            # Let's refine:
            # For each parent p:
            #   current_siblings = sorted(adj_init[p], reverse=True)
            #   target_siblings = set(adj_final[p])
            #   We need to merge all in current_siblings \ target_siblings.
            #   A node u can be merged with v if v > u.
            #   Let's pick the largest sibling in current_siblings that is NOT in target_siblings.
            #   Wait, that's not right.
            #   Let's pick the smallest sibling u that is NOT in target_siblings.
            #   We must merge it with some sibling v > u.
            #   To ensure we don't accidentally merge a target_sibling, 
            #   we can merge all non-target siblings together first, 
            #   then merge the result into a target sibling.
            #   But we can only merge if the survivor is the larger one.
            #   So if we merge all non-target siblings, the
