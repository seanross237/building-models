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
            v = int(input_data[idx])
            p = int(input_data[idx+1])
            idx += 2
            adj_init[p].append(v)
            has_parent_init[v] = True
            
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
            v = int(input_data[idx])
            p = int(input_data[idx+1])
            idx += 2
            adj_final[p].append(v)
            has_parent_final[v] = True
            
        root_final = 1
        for i in range(1, N + 1):
            if not has_parent_final[i]:
                root_final = i
                break

        # mapping[u_final] = u_initial
        # Since the problem guarantees a solution, every node in the final tree 
        # exists in the initial tree.
        # We need to find which initial node corresponds to which final node.
        # A node in the final tree is a "representative" of a set of siblings in the initial tree.
        
        # Because a merge keeps the larger value, the node in the final tree 
        # must be the maximum value among the siblings being merged.
        
        # Let's find the mapping by traversing both trees.
        # Since the structure is preserved, we can use the property that 
        # if u_final is a child of p_final, then u_initial must be a descendant 
        # of p_initial.
        
        mapping = {}
        
        # To find the mapping, we can use the fact that the final tree is a 
        # "collapsed" version of the initial tree.
        # We can perform a DFS on the final tree and match nodes.
        
        # However, a simpler way: for every node in the final tree, 
        # it must be one of the nodes in the initial tree.
        # Let's identify which initial nodes are "kept" in the final tree.
        
        is_in_final = [False] * (N + 1)
        # We don't know which nodes are in the final tree yet, 
        # but we know the structure.
        
        # Let's use the property: if u is in the final tree, its parent in the 
        # final tree is some ancestor in the initial tree.
        # But the problem says "merge two distinct sibling nodes". 
        # This means the parent remains the same.
        # So, if u is a child of p in the final tree, p must be the parent of u in the initial tree.
        # Wait, the problem says "The merged node keeps the larger value... and its children become the union".
        # This means the parent of the merged node is the same as the parent of the original siblings.
        # Therefore, the parent of a node in the final tree is the same as its parent in the initial tree.
        
        # Let's verify: if we merge siblings u and v, their parent p remains p.
        # The children of p become children(u) U children(v).
        # So the parent-child relationship (p, u) is preserved if u is the max of the merged set.
        
        # Thus, for every node u in the final tree, its parent in the final tree 
        # must be its parent in the initial tree.
        
        # Let's find the mapping:
        # For each node p in the initial tree, its children in the final tree 
        # are a subset of its children in the initial tree? No.
        # A child in the final tree is the result of merging one or more siblings in the initial tree.
        # If children of p in initial are {c1, c2, c3} and final are {c2, c3}, 
        # then c1 must have been merged into c2 or c3.
        # Since the merged node keeps the larger value, if c1 is merged into c2, 
        # then c2 > c1 and c2 is the node that remains.
        
        # Correct logic:
        # For each node p, its children in the final tree are a partition of its children in the initial tree.
        # Each group in the partition is merged into the maximum element of that group.
        
        # Let's find which initial children of p belong to which final child of p.
        # A final child 'f' of 'p' is an initial child 'i' of 'p' such that 'i' is in the final tree.
        # Wait, the problem says "The final tree uses values drawn from the same set".
        # This means the nodes in the final tree are a subset of the nodes in the initial tree.
        
        # Let's find which nodes are in the final tree.
        # A node is in the final tree if it's the root or it's a child in the final tree.
        # Actually, the problem says the final tree is a rooted tree with M nodes.
        # These M nodes are a subset of the N nodes.
        
        # Let's find the mapping:
        # For each node p in the initial tree, let its children be C_init(p).
        # Let its children in the final tree be C_final(p).
        # Every node in C_final(p) must be in C_init(p).
        # Every node in C_init(p) that is NOT in C_final(p) must be merged into some node in C_final(p).
        # Which one? The one that is its ancestor in the final tree? No, they are siblings.
        # The one that is the "representative" of the group.
        # Since the merge keeps the larger value, if we merge {c1, c2, c3} and c2 is the max, 
        # then c2 is the node that remains.
        
        # So for each p:
        # 1. Identify children of p in initial: C_init = adj_init[p]
        # 2. Identify children of p in final: C_final = adj_final[p]
        # 3. For each c in C_init:
        #    If c is not in C_final, it must be merged into some c' in C_final.
        #    Which c'? The one such that c < c' and c' is the "target".
        #    Wait, the problem says "at least one valid sequence exists".
        #    This implies that for each c in C_init \ C_final, there is a c' in C_final 
        #    such that c < c' and c' is the node that "absorbs" c.
        #    Actually, the rule is: we can merge any two siblings.
        #    If we merge c and c', the new node is max(c, c').
        #    If we want to end up with C_final, then for every c in C_init \ C_final,
        #    c must be merged into some c' in C_final such that c < c'.
        #    Is it possible that c is merged into c', and then c' is merged into c''?
        #    Yes, but that's equivalent to merging c, c', and c'' all at once.
        #    The final node will be max(c, c', c'').
        
        # Let's refine:
        # For each node p:
        #   For each child c in adj_init[p]:
        #     If c is not in adj_final[p]:
        #       Find c' in adj_final[p] such that c < c'.
        #       Wait, there might be multiple such c'. But the problem guarantees a solution.
        #       In a valid solution, each c in C_init \ C_final is merged into some c' in C_final.
        #       The only way this works is if the "representative" of the group is in C_final.
        #       Let's find for each c in C_init \ C_final, which c' in C_final it belongs to.
        #       A node c in C_init \ C_final belongs to c' in C_final if c' is the 
        #       smallest value in C_final such that c' > c and they are "connected" 
        #       through merges.
        #       Actually, the simplest way: for each c in C_init \ C_final, 
        #       it must be merged with some sibling. 
        #       Let's just find the c' in C_final that is the "target" for c.
        #       How to know which c' is the target?
        #       The problem says "The merged node keeps the larger value... and its children become the union".
        #       This means the final tree's children are a subset of the initial tree's children.
        #       Wait, that's not necessarily true. A child in the final tree could be a 
        #       descendant in the initial tree? No, the problem says "merge two distinct sibling nodes".
        #       Siblings have the same parent. So the parent remains the same.
        #       Thus, the children of p in the final tree MUST be a subset of the children of p in the initial tree.
