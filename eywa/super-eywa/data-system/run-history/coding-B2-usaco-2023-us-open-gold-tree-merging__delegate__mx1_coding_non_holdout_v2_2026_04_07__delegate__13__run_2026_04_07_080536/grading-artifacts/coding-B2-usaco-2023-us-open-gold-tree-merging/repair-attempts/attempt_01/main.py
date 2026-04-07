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
            # In a rooted tree, one is parent, one is child.
            # We need to find the root (node with no parent).
            # However, the input format "v p" usually means v is child, p is parent.
            # Let's assume v is child, p is parent.
            adj_init[v].append(u) # This is wrong if v is child. 
            # Let's re-read: "v p" describing an edge. 
            # Usually in these problems, p is parent of v.
            # Let's assume p is parent, v is child.
            # Wait, the input says "v p". Let's check standard USACO.
            # If v is child and p is parent:
            pass
        
        # Re-parsing logic:
        # The input says "v p" for N-1 lines.
        # Let's assume the first node mentioned in the edge is the child and the second is the parent.
        # Or vice versa. Let's try: p is parent of v.
        
        # Let's restart parsing properly.
        idx_reset = idx - (N-1)*2
        adj_init = [[] for _ in range(N + 1)]
        parent_init = [0] * (N + 1)
        for _ in range(N - 1):
            v = int(input_data[idx_reset])
            p = int(input_data[idx_reset+1])
            idx_reset += 2
            adj_init[p].append(v)
            parent_init[v] = p
        idx = idx_reset + (N-1)*2
        
        # Find root of initial tree
        root_init = 1
        for i in range(1, N + 1):
            if parent_init[i] == 0:
                root_init = i
                break
        
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
            
        root_final = 1
        for i in range(1, N + 1):
            if parent_final[i] == 0:
                root_final = i
                break

        # The problem: merge siblings in initial tree to get final tree.
        # A node in the final tree is a "representative" of a set of nodes in the initial tree.
        # Because a merge keeps the larger value, the node in the final tree must be 
        # the maximum value among the initial nodes it represents.
        
        # Let's map each node in the final tree to its corresponding node(s) in the initial tree.
        # Since it's guaranteed a solution exists, each node in the final tree corresponds 
        # to exactly one node in the initial tree (the one with the max value in that group).
        
        # We can find which initial node corresponds to which final node by looking at the structure.
        # A node 'u' in the final tree is the same as node 'u' in the initial tree? 
        # Not necessarily, but the values are 1..N.
        # The rule: "The merged node keeps the larger value".
        # This means if we merge nodes {2, 5}, the new node is 5.
        # So every node in the final tree MUST exist in the initial tree.
        
        # Let's find for each node in the final tree, which node in the initial tree it "is".
        # Since the values are the same, node 'u' in final is node 'u' in initial.
        # But the parent-child relationships change.
        
        # For each node u in the final tree, its children in the final tree are a subset 
        # of the children of some nodes in the initial tree.
        # Specifically, if u is a node in the final tree, its children in the final tree 
        # are the nodes that were children of the set of nodes in the initial tree 
        # that merged into u.
        
        # Let's use the property: if u is a node in the final tree, it must be a node in the initial tree.
        # Let's find the "group" of initial nodes that merge into a final node.
        # Actually, the problem is simpler: for each node u, its children in the final tree 
        # are a subset of the children of its "ancestors" in the initial tree? No.
        # Siblings are merged. This means the parent remains the same.
        # If we merge siblings a and b, their parent p remains the parent of the new node max(a, b).
        # The children of the new node are children(a) U children(b).
        
        # This means for any node u, its children in the final tree are a subset of the 
        # children of the nodes in the initial tree that merged to form u.
        # But wait, the rule says "merge two distinct sibling nodes". 
        # This means the parent does NOT change.
        # So if u is a node in the final tree, its parent in the final tree must be the same 
        # as its parent in the initial tree.
        
        # Let's verify: if we merge siblings a and b, their parent p is the same.
        # The new node is max(a, b). Its parent is still p.
        # So the parent of any node u in the final tree must be the same as its parent in the initial tree.
        # Let's check if this is true. If the parent changes, it's not a sibling merge.
        # "One operation may merge two distinct sibling nodes."
        # Yes, siblings have the same parent. So the parent of the merged node is the same.
        
        # Therefore, for every node u in the final tree, parent_final[u] == parent_init[u].
        # The only thing that changes is the set of children.
        # In the initial tree, node p has children C_init(p).
        # In the final tree, node p has children C_final(p).
        # C_final(p) must be a subset of C_init(p).
        # Wait, if C_final(p) is a subset, then some children were merged.
        # If children a, b, c are in C_init(p) and we merge a and b, the new node is max(a, b).
        # The children of max(a, b) are children(a) U children(b).
        # This means the children of a node in the final tree are the union of children 
        # of the initial nodes that merged into it.
        
        # Let's trace:
        # Initial: 1 is parent of 2, 3. 2 is parent of 4. 3 is parent of 5.
        # Merge 2 and 3: New node is 3. 3's children are {4, 5}.
        # Final: 1 is parent of 3. 3 is parent of 4, 5.
        
        # So, for each node u, we need to find which initial nodes merged into it.
        # Let S(u) be the set of initial nodes that merge into final node u.
        # 1. u is in S(u).
        # 2. For any v in S(u), if v != u, then v must be a sibling of some other node in S(u).
        # 3. The parent of all nodes in S(u) must be the same.
        # 4. The children of u in the final tree are the union of children of all v in S(u) 
        #    that are NOT in S(u) themselves? No.
        
        # Let's use the property: a node u in the final tree is the result of merging 
        # some siblings in the initial tree.
        # Let's find for each node u, which initial nodes are "under" it in the final tree.
        # Actually, the simplest way:
        # For each node p, its children in the final tree are a subset of its children in the initial tree.
        # Let's say p has children {c1, c2, ..., ck} in the initial tree.
        # In the final tree, p has children {f1, f2, ..., fm}.
        # Each fj must be one of the ci.
        # And each ci must be "absorbed" into one of the fj.
        # A child ci is absorbed into fj if ci < fj and they are siblings.
        # But wait, if ci is absorbed into fj, then fj must be a sibling of ci.
        # This means ci and fj must have the same parent.
        
        # Correct logic:
        # For each parent p:
        #   Initial children: C_init = [c1, c2, ..., ck]
        #   Final children: C_final = [f1, f2, ..., fm]
        #   Every f in C_final must be in C_init.
        #   Every c in C_init that is NOT in C_final must be merged with some
