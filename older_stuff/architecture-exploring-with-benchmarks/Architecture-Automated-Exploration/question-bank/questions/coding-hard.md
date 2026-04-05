# Hard Coding Questions — Algorithmic Reasoning

Source: Custom-crafted adversarial algorithmic reasoning problems, all verified by execution.
These problems are designed so that the naive/obvious approach gives a WRONG answer.
Each requires genuine multi-step algorithmic thinking, not language trivia.
Target difficulty: 4-5 out of 5.

---

## CODEHARD-01: Dijkstra's Blind Spot
**Domain:** Graph Algorithms
**Type:** exactMatch
**Difficulty:** 4/5

The following code uses Dijkstra's algorithm to find the shortest path from node 0 to node 3 in a weighted directed graph. What value does the function return?

```python
import heapq

def shortest_path(n, edges, src, dst):
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))

    dist = [float('inf')] * n
    dist[src] = 0
    pq = [(0, src)]
    visited = set()

    while pq:
        d, u = heapq.heappop(pq)
        if u in visited:
            continue
        visited.add(u)
        for v, w in adj[u]:
            if d + w < dist[v]:
                dist[v] = d + w
                heapq.heappush(pq, (dist[v], v))

    return dist[dst]

edges = [(0,1,2), (0,2,3), (1,3,5), (2,1,-2), (2,3,10)]
print(shortest_path(4, edges, 0, 3))
```

---

## CODEHARD-02: LRU Cache Eviction Trace
**Domain:** Data Structure Tracing
**Type:** exactMatch
**Difficulty:** 4/5

This code implements an LRU cache with capacity 3. After all operations execute, give: (a) the evictions in order as a list of `(key, value)` pairs, (b) the return values of the three `get()` calls, and (c) the final cache contents from least-recently-used to most-recently-used.

```python
from collections import OrderedDict

class LRUCache:
    def __init__(self, capacity):
        self.cache = OrderedDict()
        self.capacity = capacity

    def get(self, key):
        if key in self.cache:
            self.cache.move_to_end(key)
            return self.cache[key]
        return -1

    def put(self, key, value):
        if key in self.cache:
            self.cache.move_to_end(key)
            self.cache[key] = value
            return None
        evicted = None
        if len(self.cache) >= self.capacity:
            evicted = self.cache.popitem(last=False)
        self.cache[key] = value
        return evicted

cache = LRUCache(3)
cache.put(1, 'A')      # op 1
cache.put(2, 'B')      # op 2
cache.put(3, 'C')      # op 3
cache.get(2)            # op 4
cache.put(4, 'D')      # op 5
cache.get(1)            # op 6
cache.get(3)            # op 7
cache.put(5, 'E')      # op 8
cache.put(2, 'B*')     # op 9
cache.put(6, 'F')      # op 10
```

---

## CODEHARD-03: Knapsack Greedy Trap
**Domain:** Dynamic Programming
**Type:** exactMatch (integer)
**Difficulty:** 4/5

You have 5 items with (weight, value) pairs and a knapsack of capacity 10. What is the maximum total value achievable using a 0/1 knapsack (each item used at most once)?

```python
items = [
    (3, 5),   # Item A: weight=3, value=5, ratio=1.67
    (3, 5),   # Item B: weight=3, value=5, ratio=1.67
    (3, 5),   # Item C: weight=3, value=5, ratio=1.67
    (4, 7),   # Item D: weight=4, value=7, ratio=1.75
    (4, 7),   # Item E: weight=4, value=7, ratio=1.75
]
capacity = 10
```

Give the maximum value achievable, and which items are selected.

---

## CODEHARD-04: Floyd's Tortoise and Hare
**Domain:** Algorithm Tracing
**Type:** exactMatch
**Difficulty:** 5/5

Consider the function f(x) = (x^2 + 1) mod 55, starting from x = 2. This generates the sequence: 2, 5, 26, ...

Floyd's cycle detection algorithm is run on this sequence. The tortoise starts at f(2) and the hare starts at f(f(2)). Each step, the tortoise advances one step and the hare advances two steps. They continue until they meet.

Give: (a) the value where the tortoise and hare first meet, (b) mu (the index where the cycle begins), and (c) lambda (the length of the cycle).

---

## CODEHARD-05: Union-Find Path Compression Trace
**Domain:** Data Structure Tracing
**Type:** exactMatch
**Difficulty:** 5/5

This Union-Find uses path compression but does NOT use union-by-rank. Instead, `union(x, y)` always makes `find(y)`'s root point to `find(x)`'s root.

After all six union operations, what does `find(4)` return?

```python
class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])  # path compression
        return self.parent[x]

    def union(self, x, y):
        px, py = self.find(x), self.find(y)
        if px != py:
            self.parent[py] = px

uf = UnionFind(8)
uf.union(1, 2)
uf.union(3, 4)
uf.union(5, 6)
uf.union(2, 4)
uf.union(6, 2)
uf.union(7, 3)

print(uf.find(4))
```

Give: (a) the return value of `find(4)`, and (b) the parent array after `find(4)` completes.

---

## CODEHARD-06: Recursive Memoization with Non-Obvious Breakeven
**Domain:** Recursion / DP
**Type:** exactMatch (integer)
**Difficulty:** 4/5

What does `mystery(24)` return?

```python
memo = {}

def mystery(n):
    if n in memo:
        return memo[n]
    if n < 2:
        return n
    result = max(mystery(n // 2) + mystery(n // 3) + mystery(n // 4), n)
    memo[n] = result
    return result

print(mystery(24))
```

This function returns the maximum of either keeping `n` as-is, or recursively "splitting" it into `n//2 + n//3 + n//4`. For which values of `n` does splitting first become better than keeping?

---

## CODEHARD-07: Iterative DFS is NOT Recursive DFS
**Domain:** Graph Algorithms
**Type:** exactMatch
**Difficulty:** 4/5

This code runs an **iterative DFS** (using an explicit stack) on an undirected graph starting from node 0. What is the exact order in which nodes are visited?

```python
def dfs_iterative(graph, start):
    visited = set()
    stack = [start]
    order = []

    while stack:
        node = stack.pop()
        if node in visited:
            continue
        visited.add(node)
        order.append(node)
        for neighbor in graph[node]:
            if neighbor not in visited:
                stack.append(neighbor)

    return order

graph = {
    0: [1, 2],
    1: [0, 3, 4],
    2: [0, 4, 5],
    3: [1],
    4: [1, 2, 6],
    5: [2],
    6: [4],
}

print(dfs_iterative(graph, 0))
```

---

## CODEHARD-08: Generator Mutable Aliasing Trap
**Domain:** Output Prediction
**Type:** exactMatch
**Difficulty:** 5/5

What does `outputs` contain after this code executes? Pay careful attention to when the `result` list is mutated in-place versus replaced with a new list.

```python
def processor():
    result = []
    while True:
        x = yield result
        if x is None:
            break
        if isinstance(x, list):
            result.extend(x)
        else:
            result = [item for item in result if item != x]

proc = processor()
next(proc)  # prime the generator

outputs = []
outputs.append(proc.send([1, 2, 3]))
outputs.append(proc.send([2, 4, 5]))
outputs.append(proc.send(2))
outputs.append(proc.send([6]))
outputs.append(proc.send(4))

print(outputs)
```

Hint: Consider whether `extend()` and list comprehension reassignment produce the same object or a new one.

---

## CODEHARD-09: BFS Shortest Path Counting
**Domain:** Graph Algorithms
**Type:** exactMatch
**Difficulty:** 5/5

This code counts the number of shortest paths from node 0 to every other node in an undirected graph using BFS.

What are `count[5]` and `count[7]`?

```python
from collections import deque

def count_shortest_paths(adj, start, n):
    dist = [-1] * n
    count = [0] * n
    dist[start] = 0
    count[start] = 1
    queue = deque([start])

    while queue:
        u = queue.popleft()
        for v in adj[u]:
            if dist[v] == -1:
                dist[v] = dist[u] + 1
                count[v] = count[u]
                queue.append(v)
            elif dist[v] == dist[u] + 1:
                count[v] += count[u]

    return dist, count

adj = [[] for _ in range(8)]
edges = [(0,1),(0,2),(1,3),(1,4),(2,3),(3,5),(4,5),(5,6),(2,6),(6,7),(5,7)]
for u, v in edges:
    adj[u].append(v)
    adj[v].append(u)

dist, count = count_shortest_paths(adj, 0, 8)
print(f"count[5] = {count[5]}, count[7] = {count[7]}")
```

Give: (a) all distances from node 0, (b) all shortest-path counts, and specifically (c) the values of count[5] and count[7].

---

## CODEHARD-10: Postfix Evaluation with Truncation Division
**Domain:** Output Prediction
**Type:** exactMatch (integer)
**Difficulty:** 4/5

What does this postfix (reverse Polish notation) evaluator return for the given expression?

```python
def eval_postfix(expression):
    stack = []
    for token in expression.split():
        if token in '+-*/':
            b = stack.pop()
            a = stack.pop()
            if token == '+': stack.append(a + b)
            elif token == '-': stack.append(a - b)
            elif token == '*': stack.append(a * b)
            elif token == '/': stack.append(int(a / b))
        else:
            stack.append(int(token))
    return stack[0]

print(eval_postfix("3 8 - 2 / 5 + 7 3 2 * - /"))
```

Note: The division uses `int(a / b)` (truncation toward zero), NOT Python's `//` operator (floor division toward negative infinity). These differ for negative operands.
