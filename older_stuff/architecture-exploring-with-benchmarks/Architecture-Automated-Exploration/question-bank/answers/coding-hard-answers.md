# Answer Key — Hard Coding Questions

**WARNING: This file contains answers. Do NOT include this file in any agent context.**

All answers verified by execution on Python 3.11+.

---

## CODEHARD-01: Dijkstra's Blind Spot

| Field | Value |
|-------|-------|
| **Answer** | 7 |
| **Type** | exactMatch |
| **Common Wrong Answer** | 6 |
| **Difficulty** | 4/5 |

**Why the wrong answer is tempting:**
The true shortest path from 0 to 3 is 0->2->1->3 with cost 3+(-2)+5 = 6. A model that recognizes the negative edge might compute this correct shortest path. But the question asks what the CODE outputs, and Dijkstra's algorithm gives the wrong answer on graphs with negative edges.

**Why Dijkstra fails here:**
Dijkstra processes nodes in order of tentative distance. It visits node 1 at distance 2 (via direct edge 0->1) BEFORE discovering the cheaper path 0->2->1 at distance 1. Once node 1 is marked visited, it never gets updated. So it computes the path 0->1->3 = 7 instead of the optimal 0->2->1->3 = 6.

**Execution trace:**
- Pop (0, node 0): push (2, node 1), (3, node 2)
- Pop (2, node 1): mark visited. push (7, node 3)
- Pop (3, node 2): mark visited. push (1, node 1), (13, node 3). But node 1 is already visited!
- Pop (1, node 1): already visited, skip
- Pop (7, node 3): return 7

**Double trap:** A model that knows "Dijkstra fails on negative weights" might compute the Bellman-Ford answer (6). But the question asks what THIS code outputs.

---

## CODEHARD-02: LRU Cache Eviction Trace

| Field | Value |
|-------|-------|
| **Answer** | See below |
| **Type** | exactMatch |
| **Common Wrong Answer** | Missing the eviction at op 9 (thinking key 2 is still in cache) |
| **Difficulty** | 4/5 |

**Full answer:**
- (a) Evictions in order: `[(1, 'A'), (2, 'B'), (4, 'D'), (3, 'C')]`
- (b) get() return values: `get(2)='B'`, `get(1)=-1`, `get(3)='C'`
- (c) Final cache (LRU to MRU): `[(5, 'E'), (2, 'B*'), (6, 'F')]`

**Step-by-step trace:**

| Op | Action | Cache (LRU -> MRU) | Eviction |
|----|--------|---------------------|----------|
| 1 | put(1,A) | {1:A} | - |
| 2 | put(2,B) | {1:A, 2:B} | - |
| 3 | put(3,C) | {1:A, 2:B, 3:C} | - |
| 4 | get(2) -> 'B' | {1:A, 3:C, 2:B} | - |
| 5 | put(4,D) | {3:C, 2:B, 4:D} | **(1,'A')** |
| 6 | get(1) -> -1 | {3:C, 2:B, 4:D} | - |
| 7 | get(3) -> 'C' | {2:B, 4:D, 3:C} | - |
| 8 | put(5,E) | {4:D, 3:C, 5:E} | **(2,'B')** |
| 9 | put(2,B*) | {3:C, 5:E, 2:B*} | **(4,'D')** |
| 10 | put(6,F) | {5:E, 2:B*, 6:F} | **(3,'C')** |

**Why the wrong answer is tempting:**
The critical trap is at op 9: `put(2, 'B*')`. Key 2 was evicted at op 8, so this is a NEW insertion, not an update. This causes ANOTHER eviction (key 4). A model that believes "key 2 is still in cache because we put it earlier" will think op 9 is just an in-place update and miss the eviction of key 4. This cascading error also changes which key gets evicted at op 10.

---

## CODEHARD-03: Knapsack Greedy Trap

| Field | Value |
|-------|-------|
| **Answer** | 17 |
| **Type** | exactMatch |
| **Common Wrong Answer** | 14 |
| **Difficulty** | 4/5 |

**Correct selection:** Items A, B, D (or A, B, and either D or E) with weights 3+3+4=10, values 5+5+7=17.

**Why the wrong answer is tempting:**
The greedy approach by value/weight ratio picks items D and E first (ratio 1.75, highest). This uses weight 4+4=8, leaving capacity 2. No remaining item fits (all have weight >= 3). Greedy total: 7+7=14.

The optimal solution picks two weight-3 items and one weight-4 item: 5+5+7=17. The greedy approach is suboptimal because picking the two "best ratio" items together wastes 2 units of capacity, while three lighter items can fully utilize the knapsack.

---

## CODEHARD-04: Floyd's Tortoise and Hare

| Field | Value |
|-------|-------|
| **Answer** | meeting value=37, mu=2, lambda=6 |
| **Type** | exactMatch |
| **Common Wrong Answer** | Arithmetic errors on modular squaring, or confusing tortoise/hare positions |
| **Difficulty** | 5/5 |

**The sequence:** 2, 5, 26, 17, 15, 6, 37, 50, 26, 17, 15, 6, 37, 50, ...

**Key modular arithmetic:**
- f(2) = 5
- f(5) = 26
- f(26) = 677 mod 55 = 17
- f(17) = 290 mod 55 = 15
- f(15) = 226 mod 55 = 6
- f(6) = 37
- f(37) = 1370 mod 55 = 50
- f(50) = 2501 mod 55 = 26 (cycle back)

**Phase 1 (meeting point) trace:**

| Step | Tortoise | Hare (two steps) |
|------|----------|-------------------|
| Init | 5 | 26 |
| 1 | 26 | f(f(26))=f(17)=15 |
| 2 | 17 | f(f(15))=f(6)=37 |
| 3 | 15 | f(f(37))=f(50)=26 |
| 4 | 6 | f(f(26))=f(17)=15 |
| 5 | 37 | f(f(15))=f(6)=37 |

**Meet at value 37.**

**Phase 2:** Reset tortoise to start (2), keep hare at 37. Both advance one step:
- Step 1: tortoise=5, hare=50
- Step 2: tortoise=26, hare=26. Meet!

**mu = 2** (cycle starts at position 2, which is value 26).

**Phase 3:** From meeting point 26, advance one pointer: 26->17->15->6->37->50->26. Count = **6 = lambda**.

**Why this is hard:**
The model must correctly compute multiple modular squares (26^2+1, 37^2+1, 50^2+1) and track both pointers simultaneously. A single arithmetic error derails the entire trace.

---

## CODEHARD-05: Union-Find Path Compression Trace

| Field | Value |
|-------|-------|
| **Answer** | find(4) = 7; parent = [0, 5, 1, 7, 7, 7, 5, 7] |
| **Type** | exactMatch |
| **Common Wrong Answer** | find(4) = 1 (ignoring path compression effects during union calls) |
| **Difficulty** | 5/5 |

**Step-by-step trace:**

| Operation | Action | Parent Array |
|-----------|--------|--------------|
| Initial | - | [0,1,2,3,4,5,6,7] |
| union(1,2) | find(1)=1, find(2)=2, set parent[2]=1 | [0,1,1,3,4,5,6,7] |
| union(3,4) | find(3)=3, find(4)=4, set parent[4]=3 | [0,1,1,3,3,5,6,7] |
| union(5,6) | find(5)=5, find(6)=6, set parent[6]=5 | [0,1,1,3,3,5,5,7] |
| union(2,4) | find(2)=1, find(4)=3, set parent[3]=1 | [0,1,1,1,3,5,5,7] |
| union(6,2) | find(6)=5, find(2)=1, set parent[1]=5 | [0,5,1,1,3,5,5,7] |
| union(7,3) | find(7)=7, find(3)=? (see below), set parent[5]=7 | [0,5,1,5,3,7,5,7] |

**Critical step: find(3) during union(7,3):**
- parent[3]=1 -> find(1)
- parent[1]=5 -> find(5)
- parent[5]=5 -> return 5
- Path compression: parent[1]=5 (already), parent[3]=5
- So find(3)=5, and then parent[5]=7 (not parent[1]=7!)

**Then find(4):**
- parent[4]=3 -> find(3)
- parent[3]=5 -> find(5)
- parent[5]=7 -> find(7)
- parent[7]=7 -> return 7
- Path compression: parent[5]=7, parent[3]=7, parent[4]=7
- Final parent: [0, 5, 1, 7, 7, 7, 5, 7]

**Why this is hard:**
Path compression happens DURING the find() calls inside union(). The union(6,2) call changes parent[1] to 5, and union(7,3) triggers find(3) which follows the chain 3->1->5 and sets parent[5]=7. Without tracking these intermediate path compressions, you'll get the wrong root. Most models will trace the unions without accounting for path compression side effects.

---

## CODEHARD-06: Recursive Memoization with Non-Obvious Breakeven

| Field | Value |
|-------|-------|
| **Answer** | 27 |
| **Type** | exactMatch |
| **Common Wrong Answer** | 24 or 26 |
| **Difficulty** | 4/5 |

**Recursion tree (key values):**

| n | n//2 | n//3 | n//4 | Split sum | max(split, n) |
|---|------|------|------|-----------|---------------|
| 1 | - | - | - | - | 1 |
| 2 | 1 | 0 | 0 | 1 | **2** (keep) |
| 3 | 1 | 1 | 0 | 2 | **3** (keep) |
| 4 | 2 | 1 | 1 | 4 | **4** (tie) |
| 6 | 3 | 2 | 1 | 6 | **6** (tie) |
| 8 | 4 | 2 | 2 | 8 | **8** (tie) |
| **12** | 6 | 4 | 3 | **13** | **13** (split!) |
| 24 | 13 | 8 | 6 | **27** | **27** (split!) |

**The breakeven:** n=12 is the first value where splitting beats keeping (6+4+3=13 > 12).

**Why the wrong answer is tempting:**
- A model that assumes mystery(n) = n for all n will return 24 (the most common wrong answer)
- A model that correctly identifies the split at n=24 but uses mystery(12)=12 instead of 13 will get 12+8+6=26
- Only by correctly computing mystery(12)=13 does the chain propagate to give 27

---

## CODEHARD-07: Iterative DFS is NOT Recursive DFS

| Field | Value |
|-------|-------|
| **Answer** | [0, 2, 5, 4, 6, 1, 3] |
| **Type** | exactMatch |
| **Common Wrong Answer** | [0, 1, 3, 4, 2, 5, 6] (recursive DFS order) |
| **Difficulty** | 4/5 |

**Why iterative and recursive DFS differ:**
In iterative DFS, neighbors are pushed onto the stack in the order they appear in the adjacency list. Since a stack is LIFO, the LAST neighbor pushed is the FIRST one popped. For node 0 with neighbors [1, 2]: 1 is pushed first, then 2. So 2 is popped first.

In recursive DFS, neighbors are visited in the order they appear: 1 is visited first.

**Iterative DFS trace:**

| Step | Stack (top right) | Action | Order |
|------|-------------------|--------|-------|
| 0 | [0] | Pop 0, visit. Push 1, 2 | [0] |
| 1 | [1, 2] | Pop 2, visit. Push 4, 5 | [0, 2] |
| 2 | [1, 4, 5] | Pop 5, visit. (2 already visited) | [0, 2, 5] |
| 3 | [1, 4] | Pop 4, visit. Push 6 (1,2 visited) | [0, 2, 5, 4] |
| 4 | [1, 6] | Pop 6, visit. (4 visited) | [0, 2, 5, 4, 6] |
| 5 | [1] | Pop 1, visit. Push 3 (0,4 visited) | [0, 2, 5, 4, 6, 1] |
| 6 | [3] | Pop 3, visit. (1 visited) | [0, 2, 5, 4, 6, 1, 3] |

**Why the wrong answer is tempting:**
Most textbooks teach recursive DFS. The vast majority of people (and models) mentally trace DFS as "visit first neighbor, recurse." The iterative version with an explicit stack reverses the neighbor visit order, which changes the entire traversal. This is a well-known but frequently forgotten distinction.

---

## CODEHARD-08: Generator Mutable Aliasing Trap

| Field | Value |
|-------|-------|
| **Answer** | `[[1,2,3,2,4,5], [1,2,3,2,4,5], [1,3,4,5,6], [1,3,4,5,6], [1,3,5,6]]` |
| **Type** | exactMatch |
| **Common Wrong Answer** | `[[1,2,3], [1,2,3,2,4,5], [1,3,4,5], [1,3,4,5,6], [1,3,5,6]]` |
| **Difficulty** | 5/5 |

**The mechanism:**
- `result.extend(x)` modifies the list IN PLACE (same object)
- `result = [comprehension]` creates a NEW list object
- `yield result` yields a REFERENCE to the current list object, not a copy

**Detailed trace:**

| send() | x | Action | result object | Yielded reference |
|--------|---|--------|---------------|-------------------|
| [1,2,3] | list | extend (in-place) | Object A = [1,2,3] | -> A |
| [2,4,5] | list | extend (in-place) | Object A = [1,2,3,2,4,5] | -> A |
| 2 | int | reassign (new list) | Object B = [1,3,4,5] | -> B |
| [6] | list | extend (in-place) | Object B = [1,3,4,5,6] | -> B |
| 4 | int | reassign (new list) | Object C = [1,3,5,6] | -> C |

**The aliasing:**
- `outputs[0]` and `outputs[1]` both reference Object A
- After the second `send()`, Object A has been extended to [1,2,3,2,4,5]
- So outputs[0] retroactively shows [1,2,3,2,4,5] instead of [1,2,3]!
- Similarly, outputs[2] and outputs[3] both reference Object B = [1,3,4,5,6]
- `o0 is o1` evaluates to `True` (same object)
- `o2 is o3` evaluates to `True` (same object)

**Why the wrong answer is tempting:**
The "obvious" trace records each yield's value at the moment it happens: [1,2,3], [1,2,3,2,4,5], [1,3,4,5], [1,3,4,5,6], [1,3,5,6]. But `extend()` mutates the same list object, so earlier entries in `outputs` get updated retroactively. Models rarely track object identity through generator yields.

---

## CODEHARD-09: BFS Shortest Path Counting

| Field | Value |
|-------|-------|
| **Answer** | count[5]=4, count[7]=1 |
| **Type** | exactMatch |
| **Common Wrong Answer** | count[7]>1 (thinking the 5->7 edge contributes) |
| **Difficulty** | 5/5 |

**Full answer:**
- Distances: [0, 1, 1, 2, 2, 3, 2, 3]
- Path counts: [1, 1, 1, 2, 1, 4, 1, 1]

**Graph structure:**
Edges: 0-1, 0-2, 1-3, 1-4, 2-3, 3-5, 4-5, 5-6, 2-6, 6-7, 5-7

**BFS trace (from node 0):**

| Process | Neighbor | dist update | count update |
|---------|----------|-------------|-------------|
| 0 | 1 | dist[1]=1 | count[1]=1 |
| 0 | 2 | dist[2]=1 | count[2]=1 |
| 1 | 3 | dist[3]=2 | count[3]=1 |
| 1 | 4 | dist[4]=2 | count[4]=1 |
| 2 | 3 | dist[3]==2==1+1 | count[3]+=1 -> **2** |
| 2 | 6 | dist[6]=2 | count[6]=1 |
| 3 | 5 | dist[5]=3 | count[5]=count[3]=**2** |
| 4 | 5 | dist[5]==3==2+1 | count[5]+=count[4]=1 -> **3** |
| 6 | 7 | dist[7]=3 | count[7]=count[6]=**1** |
| 6 | 5 | dist[5]==3==2+1 | count[5]+=count[6]=1 -> **4** |
| 5 | 7 | dist[7]==3, dist[5]+1==4, 3!=4 | **NO UPDATE** |

**Why count[7]=1 is surprising:**
Node 7 is connected to both node 5 (4 shortest paths) and node 6 (1 shortest path). But the edge 5->7 does NOT contribute shortest paths because dist[5]=3 and dist[7]=3. The condition `dist[7] == dist[5] + 1` (i.e., 3 == 4) is FALSE. Node 7 was first reached from node 6 at distance 3, and no other path at distance 3 reaches it.

The 4 shortest paths to node 5 are: 0-1-3-5, 0-2-3-5, 0-1-4-5, 0-2-6-5. None of these extend to a shortest path to node 7 because that would require distance 4.

---

## CODEHARD-10: Postfix Evaluation with Truncation Division

| Field | Value |
|-------|-------|
| **Answer** | 3 |
| **Type** | exactMatch |
| **Common Wrong Answer** | 2 (using floor division //) or -7 (reversing operand order) |
| **Difficulty** | 4/5 |

**Expression:** `3 8 - 2 / 5 + 7 3 2 * - /`

**Step-by-step trace:**

| Token | Stack (before) | Action | Stack (after) |
|-------|---------------|--------|---------------|
| 3 | [] | push | [3] |
| 8 | [3] | push | [3, 8] |
| - | [3, 8] | a=3, b=8, 3-8=-5 | [-5] |
| 2 | [-5] | push | [-5, 2] |
| / | [-5, 2] | a=-5, b=2, int(-5/2)=**-2** | [-2] |
| 5 | [-2] | push | [-2, 5] |
| + | [-2, 5] | -2+5=3 | [3] |
| 7 | [3] | push | [3, 7] |
| 3 | [3, 7] | push | [3, 7, 3] |
| 2 | [3, 7, 3] | push | [3, 7, 3, 2] |
| * | [3, 7, 3, 2] | 3*2=6 | [3, 7, 6] |
| - | [3, 7, 6] | a=7, b=6, 7-6=1 | [3, 1] |
| / | [3, 1] | int(3/1)=3 | [3] |

**Answer: 3**

**Why the wrong answer is tempting:**

**Trap 1: int() vs //**
`int(-5/2) = int(-2.5) = -2` (truncation toward zero)
`-5 // 2 = -3` (floor toward negative infinity)
If the model uses `//` instead of `int(a/b)`: -3+5=2, then 2/1=2. Wrong answer: **2**.

**Trap 2: Operand order**
In postfix, `a b -` means `a - b`. When popping from the stack, `b` is popped first, then `a`. If the model reverses this: `3 8 -` becomes 8-3=5 instead of 3-8=-5. This changes the subsequent division (no negative number = no truncation trap), giving a completely different answer.

---

## Summary Table

| ID | Answer | Type | Common Wrong Answer | Why Wrong | Difficulty |
|----|--------|------|---------------------|-----------|------------|
| CODEHARD-01 | 7 | exactMatch | 6 | Computes true shortest path instead of Dijkstra's output | 4/5 |
| CODEHARD-02 | evictions: [(1,A),(2,B),(4,D),(3,C)]; final: [(5,E),(2,B*),(6,F)] | exactMatch | Missing eviction at op 9 | Thinks key 2 is still cached after eviction at op 8 | 4/5 |
| CODEHARD-03 | 17 | exactMatch | 14 | Applies greedy by value/weight ratio | 4/5 |
| CODEHARD-04 | meeting=37, mu=2, lambda=6 | exactMatch | Various arithmetic errors | Modular squaring errors cascade | 5/5 |
| CODEHARD-05 | find(4)=7; parent=[0,5,1,7,7,7,5,7] | exactMatch | find(4)=1 | Ignores path compression side effects during union | 5/5 |
| CODEHARD-06 | 27 | exactMatch | 24 or 26 | Assumes mystery(n)=n always, or misses mystery(12)=13 | 4/5 |
| CODEHARD-07 | [0,2,5,4,6,1,3] | exactMatch | [0,1,3,4,2,5,6] | Traces recursive DFS instead of iterative (stack reversal) | 4/5 |
| CODEHARD-08 | [[1,2,3,2,4,5],[1,2,3,2,4,5],[1,3,4,5,6],[1,3,4,5,6],[1,3,5,6]] | exactMatch | [[1,2,3],[1,2,3,2,4,5],[1,3,4,5],[1,3,4,5,6],[1,3,5,6]] | Doesn't track mutable aliasing through generator yields | 5/5 |
| CODEHARD-09 | count[5]=4, count[7]=1 | exactMatch | count[7]>1 | Thinks edge 5-7 contributes to shortest paths to 7 | 5/5 |
| CODEHARD-10 | 3 | exactMatch | 2 | Uses // instead of int(a/b) for negative division | 4/5 |
