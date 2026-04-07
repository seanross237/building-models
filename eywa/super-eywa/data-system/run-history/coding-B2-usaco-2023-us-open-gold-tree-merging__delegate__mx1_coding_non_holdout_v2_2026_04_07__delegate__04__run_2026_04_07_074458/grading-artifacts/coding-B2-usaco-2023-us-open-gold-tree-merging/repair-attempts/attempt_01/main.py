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
            p = int(input_data[idx+1])
            idx += 2
            adj_init[p].append(u)
            parent_init[u] = p
            
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

        # Find roots
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

        # The problem guarantees a valid sequence exists.
        # A merge operation: merge two siblings, keep the larger value.
        # This means for any node in the final tree, it must be the maximum 
        # value among the set of initial nodes that were merged into it.
        # Also, all children of the final node must be descendants of the 
        # initial nodes that formed it.
        
        # To find the merges:
        # For every node u in the initial tree, if its parent in the initial tree
        # is different from its parent in the final tree, it must have been merged
        # into a sibling.
        
        # However, the rule is: merge two siblings.
        # Let's track the current parent of each node.
        # Initially, parent[i] = parent_init[i].
        # We want to reach parent[i] = parent_final[i].
        
        # A node u needs to be merged if parent_init[u] != parent_final[u].
        # If parent_init[u] != parent_final[u], u must be merged with a sibling
        # such that the resulting node's parent is parent_final[u].
        # But the problem says "merge two distinct sibling nodes". 
        # This implies the parent remains the same.
        # Wait, if we merge siblings u and v, the new node has the same parent.
        # So the parent of the merged node is the same as the parent of u and v.
        # This means the parent of a node can only change if the node itself is merged.
        # If u is merged into v, u "disappears" and v takes its children.
        # The parent of v is the same as the parent of u.
        
        # Therefore, for any node u, if parent_init[u] != parent_final[u],
        # it's impossible unless the parent itself changed? No.
        # If u is merged into v, u is gone. The children of u become children of v.
        # The parent of v is the same as the parent of u.
        # So the only way for a node's parent to "change" is if the node is merged.
        # But the problem says "the merged node keeps the larger value".
        # This means if we merge u and v (u < v), u is gone, v remains.
        # The parent of v is the same as the parent of u.
        
        # Let's re-read: "One operation may merge two distinct sibling nodes. 
        # The merged node keeps the larger value... and its children become the union..."
        # This means the parent of the merged node is the same as the parent of the siblings.
        # So the parent of any node that survives a merge is the same as its original parent.
        # Thus, for all nodes u that exist in the final tree, parent_init[u] must equal parent_final[u].
        
        # Let's identify which nodes are merged.
        # A node u is merged if it does not exist in the final tree.
        # A node u exists in the final tree if it is a node in the final tree structure.
        # Since the set of values is the same, the nodes in the final tree are a subset of 1..N.
        
        # For each node u in the initial tree:
        # If u is not in the final tree, it must be merged into some sibling v.
        # Which sibling? The one that is "larger" and eventually becomes the representative.
        # Actually, the problem says "any valid sequence".
        # Let's find for each node u in the initial tree, which node it ends up being merged into.
        # If u is in the final tree, it's its own representative.
        # If u is not in the final tree, it must be merged into a sibling.
        
        # Let's use the property: if u is merged into v, then parent_init[u] == parent_init[v]
        # and u < v.
        # We can find the target representative for each node.
        # For each node u, if u is in the final tree, its representative is u.
        # If u is not in the final tree, its representative is the node in the final tree
        # that is its ancestor in the initial tree and is a sibling (or sibling of sibling...).
        # Actually, the simplest way:
        # For each node u, if parent_init[u] != parent_final[u], it's impossible? 
        # No, the parent of u in the final tree is the parent of the node u was merged into.
        # But the parent of the merged node is the same as the parent of the siblings.
        # So parent_final[u] must be the same as parent_init[u] for all u in the final tree.
        
        # Let's find which nodes are "lost".
        # A node u is lost if it's not in the final tree.
        # For each lost node u, it must be merged with a sibling v such that v > u.
        # To ensure we don't merge a node that is already a representative,
        # we can process nodes from bottom to top.
        
        # Let's find the set of nodes present in the final tree.
        final_nodes = set()
        for i in range(1, N + 1):
            if parent_final[i] != 0 or i == root_final:
                # This is slightly wrong, all nodes 1..N are in the initial tree.
                # The final tree is a subset of these nodes? 
                # "The final tree uses values drawn from the same set."
                # "The final tree has M nodes." (implied by M-1 edges)
                pass
        
        # Correct approach:
        # The final tree is a structure with M nodes.
        # Let's identify which nodes from the initial tree are in the final tree.
        # A node u is in the final tree if it's one of the M nodes.
        # We can find these M nodes by looking at the edges.
        # Wait, the input for the final tree is M-1 edges. So there are M nodes.
        # Which M nodes? The problem says "values drawn from the same set".
        # It doesn't say which ones. But it says "at least one valid sequence exists".
        # This implies the M nodes in the final tree are a subset of the N nodes.
        
        # Let's find the M nodes in the final tree.
        final_nodes_set = set()
        # The edges are (v, p). The nodes are v and p.
        # But we need to be careful. The root might not be in an edge.
        # Let's collect all nodes mentioned in the M-1 edges.
        # And the root.
        
        # Actually, the input format for final tree is:
        # M
        # M-1 lines of v p
        # This means there are M nodes.
        # Let's find them.
        final_nodes_list = []
        # We need to find the root of the final tree first.
        # The root is the node that is never a 'v' in the 'v p' edges.
        # Wait, 'v p' means v is child, p is parent.
        # So the root is the node that is never a 'v'.
        
        # Let's re-read: "v p describing an edge". Usually this means v is child, p is parent.
        # Let's assume v is child, p is parent.
        
        # Let's find the M nodes.
        # The nodes are the ones that appear in the M-1 edges, plus the root.
        # But we don't know the root.
        # Let's find the root by checking which node has no parent.
        
        # Let's re-parse the final tree.
        # We'll use a dictionary to store the final tree structure.
        final_adj = {}
        final_parent = {}
        nodes_in_final = set()
        
        # We need to find the root of the final tree.
        # The root is the node that is not a child of any other node.
        # Let's collect all children and all parents.
        children_final = set()
        parents_final = set()
        
        # We need to read M-1 edges.
        # The edges are given as v p.
        # Let's store them.
        edges_final =
