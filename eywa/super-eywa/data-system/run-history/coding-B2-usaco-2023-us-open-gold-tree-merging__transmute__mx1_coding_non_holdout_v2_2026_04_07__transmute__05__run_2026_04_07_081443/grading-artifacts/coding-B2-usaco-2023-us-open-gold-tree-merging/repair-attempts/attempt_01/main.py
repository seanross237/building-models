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
        has_parent_init = [False] * (N + 1)
        for _ in range(N - 1):
            u = int(input_data[idx])
            p = int(input_data[idx+1])
            idx += 2
            adj_init[p].append(u)
            parent_init[u] = p
            has_parent_init[u] = True
            
        root_init = 1
        for i in range(1, N + 1):
            if not has_parent_init[i]:
                root_init = i
                break
                
        M = int(input_data[idx])
        idx += 1
        adj_final = [[] for _ in range(N + 1)]
        parent_final = [0] * (N + 1)
        has_parent_final = [False] * (N + 1)
        for _ in range(M - 1):
            u = int(input_data[idx])
            p = int(input_data[idx+1])
            idx += 2
            adj_final[p].append(u)
            parent_final[u] = p
            has_parent_final[u] = True
            
        root_final = 1
        for i in range(1, N + 1):
            if not has_parent_final[i]:
                root_final = i
                break

        # mapping[u_init] = u_final
        # Since we merge siblings, a node in the final tree is the max value 
        # of a set of siblings in the initial tree.
        # Because a solution is guaranteed, we can find the mapping by 
        # looking at the parent-child relationships.
        
        mapping = [0] * (N + 1)
        
        # To find mapping: for each node in initial tree, its parent in final tree
        # must be the node that its parent in initial tree maps to.
        # However, the root is special.
        
        # Let's use the property: if u is a child of p in initial, 
        # then mapping[u] is a child of mapping[p] in final.
        # We can determine mapping[u] by looking at the structure.
        # Since we only merge siblings, the parent of a node in the final tree
        # is the same as the parent of the node in the initial tree (after mapping).
        
        # A more reliable way:
        # For each node u in initial, its final representative is the node v in final
        # such that u is in the subtree of v in the initial tree AND v is in the 
        # subtree of root_final.
        # Actually, the problem says: "The merged node keeps the larger value".
        # This means if we merge siblings {a, b}, the new node is max(a, b).
        # So for any node v in the final tree, v must be one of the nodes in the initial tree.
        # And all nodes in the initial tree that map to v must have v as their max value.
        
        # Let's find mapping[u] for all u.
        # For the root: mapping[root_init] = root_final.
        # For any other u: mapping[u] is a child of mapping[parent_init[u]] in the final tree.
        # Which child? The one that contains u in its "initial" subtree.
        
        mapping = [0] * (N + 1)
        mapping[root_init] = root_final
        
        # We need to know which final-child contains which initial-node.
        # Since we only merge siblings, the set of initial-nodes that map to a final-node v
        # are all siblings in the initial tree (or descendants of siblings that merged).
        # Actually, the simplest way: mapping[u] is the node v in final tree such that
        # u is in the subtree of v in the initial tree, and v is a child of mapping[parent_init[u]].
        
        # Let's pre-calculate subtree sets for final tree nodes.
        # But we don't know the mapping yet.
        # Let's use the property: if u is a child of p in initial, 
        # then mapping[u] is a child of mapping[p] in final.
        # We can find mapping[u] by checking which child of mapping[p] in final
        # has u in its subtree in the initial tree.
        
        # Precompute initial subtrees
        subtree_init = [set() for _ in range(N + 1)]
        def get_subtrees(u):
            subtree_init[u].add(u)
            for v in adj_init[u]:
                get_subtrees(v)
                subtree_init[u].update(subtree_init[v])
        
        get_subtrees(root_init)
        
        # BFS/DFS to fill mapping
        stack = [root_init]
        while stack:
            u = stack.pop()
            p_final = mapping[parent_init[u]] if u != root_init else root_final
            # If u is root, it's already mapped.
            if u == root_init:
                continue
                
            # Find which child of p_final in final tree contains u in its initial subtree
            # Wait, the final tree structure is given. The children of p_final are adj_final[p_final].
            # One of these children v must have u in its initial subtree.
            # But the final tree is built from the initial tree.
            # A node v in the final tree is a "representative" of some initial nodes.
            # The children of v in the final tree are the representatives of the children of those initial nodes.
            
            # Let's use the property: mapping[u] is the node v in final tree such that
            # v is a child of mapping[parent_init[u]] AND u is in the subtree of v in the initial tree.
            # This is still slightly circular. Let's use the fact that the final tree 
            # is a "compressed" version of the initial tree.
            
            # Correct logic:
            # For each node u in initial, mapping[u] is the node v in final such that
            # u is in the subtree of v in the initial tree, and v is a child of mapping[parent_init[u]].
            # Since we don't know which v, we can use the fact that the final tree nodes 
            # are a subset of the initial nodes.
            # For each node v in the final tree, it "covers" a set of nodes in the initial tree.
            # Let's find which v covers which u.
            # A node v in the final tree is a node in the initial tree.
            # v covers u if u is in the subtree of v in the initial tree AND 
            # there is no node w in the final tree such that w is a child of v and u is in the subtree of w.
            
            # Let's find mapping[u] for all u:
            # 1. For each v in final tree, it is a node in the initial tree.
            # 2. For each v in final tree, its children in final tree are some nodes in initial tree.
            # 3. A node u in initial tree maps to v in final tree if v is the "closest" 
            #    ancestor of u in the final tree structure.
            
            # Let's find the mapping by traversing the final tree.
            # For a node v in final, its children are c1, c2, ... in final.
            # These children c_i must be descendants of v in the initial tree.
            # Specifically, each c_i is the max value of some set of siblings in the initial tree.
            
            # Let's use a different approach:
            # For each node u in initial, its parent in final is mapping[parent_init[u]].
            # This is only true if u is not merged with its siblings.
            # If u is merged with siblings, mapping[u] = mapping[sibling].
            
            # Let's find for each u in initial, which v in final it belongs to.
            # v is the node in the final tree such that u is in the subtree of v in the initial tree,
            # and there is no child w of v in the final tree such that u is in the subtree of w in the initial tree.
            
            # This can be done by:
            # For each v in final, mark all u in its initial subtree.
            # Then for each u, the mapping[u] is the v with the smallest subtree_init[v] that contains u.
            
            # Wait, the problem says "The merged node keeps the larger value".
            # This means if we merge siblings {2, 5}, the new node is 5.
            # So the nodes in the final tree are a subset of the nodes in the initial tree.
            # And for any node v in the final tree, v must be the maximum value among the 
            # initial nodes it represents.
            
            # Let's find mapping[u] for all u:
            # For each u in initial, mapping[u] = v if:
            # 1. v is in the final tree.
            # 2. u is in the subtree of v in the initial tree.
            # 3. There is no child w of v in the final tree such that u is in the subtree of w in the initial tree.
            
            # This is easy to implement.
            pass

        # Re-implementing mapping logic
        mapping = [0] * (N + 1)
        #
