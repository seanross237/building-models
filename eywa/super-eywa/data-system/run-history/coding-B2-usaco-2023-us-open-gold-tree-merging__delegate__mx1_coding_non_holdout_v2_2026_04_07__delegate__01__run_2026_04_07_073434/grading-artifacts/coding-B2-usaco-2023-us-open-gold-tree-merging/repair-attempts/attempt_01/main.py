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
            # The problem says v p, but usually it's child parent or parent child.
            # Given "v p describing an edge", and it's a rooted tree, 
            # we need to find the root (node with no parent).
            # Let's assume v is child, p is parent based on "v p".
            adj_init[v].append(u) # This is wrong if v is child. 
            # Let's re-read: "v p describing an edge". 
            # In USACO, usually it's child parent or parent child.
            # Let's assume p is parent of v.
            pass 
        
        # Re-parsing logic:
        # The input format "v p" for N-1 lines means we need to identify the root.
        # Let's use a more robust way to build the tree.
        
        # Resetting idx for this test case
        # Actually, let's just read N-1 edges.
        
        # Since the problem says "v p", let's assume p is parent of v.
        # We'll find the root by finding the node that is never a 'v'.
        
        # Wait, the input says "v p". Let's assume p is parent of v.
        # Let's collect all edges.
        edges_init = []
        has_parent_init = [False] * (N + 1)
        for _ in range(N - 1):
            v = int(input_data[idx])
            p = int(input_data[idx+1])
            idx += 2
            edges_init.append((v, p))
            has_parent_init[v] = True
            
        root_init = 1
        for i in range(1, N + 1):
            if not has_parent_init[i]:
                root_init = i
                break
        
        children_init = [[] for _ in range(N + 1)]
        parent_init = [0] * (N + 1)
        for v, p in edges_init:
            children_init[p].append(v)
            parent_init[v] = p

        M = int(input_data[idx])
        idx += 1
        edges_final = []
        has_parent_final = [False] * (N + 1)
        for _ in range(M - 1):
            v = int(input_data[idx])
            p = int(input_data[idx+1])
            idx += 2
            edges_final.append((v, p))
            has_parent_final[v] = True
            
        root_final = 1
        for i in range(1, N + 1):
            if not has_parent_final[i]:
                root_final = i
                break
                
        children_final = [[] for _ in range(N + 1)]
        parent_final = [0] * (N + 1)
        for v, p in edges_final:
            children_final[p].append(v)
            parent_final[v] = p

        # To transform initial to final:
        # For each node in the final tree, its children must be a subset of 
        # the children of some node in the initial tree (after some merges).
        # Because a merge keeps the larger value, the final node must be 
        # the maximum value among the initial nodes that were merged into it.
        
        # The problem guarantees a solution exists.
        # This means for every node u in the final tree, there is a unique node 
        # in the initial tree that "represents" it. Let's call this mapping map(u_final) = u_init.
        # Since the merge rule is: merge(a, b) -> max(a, b), 
        # the node u_final must be the max of all initial nodes that merged into it.
        
        # Let's find which initial node corresponds to which final node.
        # A node u in the initial tree is "kept" if it exists in the final tree.
        # If a node is not in the final tree, it must have been merged into a sibling.
        
        # Let's identify the "surviving" nodes.
        # A node is a survivor if it is a child of a survivor in the final tree.
        # The root is always a survivor.
        
        survivors = [False] * (N + 1)
        survivors[root_final] = True # This is not quite right. 
        # The values are the same. The structure changes.
        # Let's find which initial nodes are present in the final tree.
        # Actually, the set of nodes is the same. The final tree is just a different structure.
        # The nodes in the final tree are 1..N.
        
        # Let's find for each node in the final tree, which node in the initial tree it "is".
        # Since the merge rule says max(a, b) survives, the node 'v' in the final tree
        # must be the maximum value among all initial nodes that were merged into it.
        
        # Let's use the property: if node 'u' is in the final tree, it must have been 
        # an initial node. If it's a child of 'p' in the final tree, it must have 
        # been a descendant of 'p' in the initial tree? No, that's not right.
        # The rule is: "merge two distinct sibling nodes".
        # This means the parent remains the same.
        # So, if u and v are siblings in the initial tree, they can be merged.
        # Their parent remains the same. The new node is max(u, v).
        # This means the parent-child relationships only change by reducing the number of children.
        # The parent of a node in the final tree must be the same as the parent in the initial tree.
        
        # Let's verify: "The merged node keeps the larger value... its children become the union".
        # This means the parent of the merged node is the same as the parent of the original nodes.
        # Therefore, for any node u in the final tree, its parent in the final tree 
        # must be the same as its parent in the initial tree.
        
        # Let's check this assumption. If parent(u) in final is different from parent(u) in initial,
        # then the only way is if the parent itself was merged. But merging siblings 
        # doesn't change the parent of the siblings.
        # So, for every node u that is NOT merged, parent_final(u) == parent_init(u).
        # If u is merged into v, then parent_final(v) == parent_init(v) == parent_init(u).
        
        # So, for each parent p, the set of children in the final tree must be a subset 
        # of the children in the initial tree.
        # Specifically, if children_final(p) = {c1, c2, ...}, then these must be 
        # a subset of children_init(p).
        # Any child in children_init(p) that is NOT in children_final(p) must have been 
        # merged into one of the children in children_final(p).
        # Which one? The one that is larger.
        
        merges = []
        for p in range(1, N + 1):
            # Children of p in initial
            init_c = set(children_init[p])
            # Children of p in final
            final_c = set(children_final[p])
            
            # Nodes in init_c but not in final_c must be merged into someone in final_c
            to_merge = init_c - final_c
            
            # For each node in to_merge, it must be merged with a sibling in final_c 
            # that is larger than it.
            # Wait, the rule is "merge two distinct sibling nodes".
            # We can merge a node in to_merge with a node in final_c, or with another node in to_merge.
            # To eventually end up with only final_c, each node in to_merge must be 
            # merged into some node in final_c.
            # The rule is: merge(a, b) -> max(a, b).
            # So if we merge 'u' (from to_merge) and 'v' (from final_c), 
            # the survivor is max(u, v). 
            # But the final tree MUST have 'v' as a child. 
            # This is only possible if v > u.
            
            # Let's sort to_merge and final_c to make it easier.
            # Actually, the problem guarantees a solution exists.
            # This means for every u in to_merge, there is a v in final_c such that v > u.
            # Or, u can be merged with another u' in to_merge, and then the result 
            # is merged with a v in final_c.
            
            # Let's use a greedy approach for each parent:
            # While there are nodes in to_merge:
            #   Pick the largest node in to_merge, say 'u'.
            #   Find the smallest node in final_c that is > u.
            #   Merge u and that node.
            #   Wait, if we merge u and v, and
