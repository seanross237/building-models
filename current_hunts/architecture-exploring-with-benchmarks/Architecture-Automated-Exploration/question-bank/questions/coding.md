# Coding Questions — Code Reasoning

Source: Custom-crafted algorithmic reasoning problems, all verified by execution.
Tests code reasoning and algorithmic thinking, not implementation ability.
Each problem has at least one plausible-but-wrong answer from common reasoning shortcuts.

---

## CODE-01: Self-Referential Array Mutation
**Domain:** Output Prediction
**Type:** exactMatch

What does the following Python code return?

```python
def transform(arr):
    n = len(arr)
    for i in range(n):
        arr[i] = arr[arr[i] % n]
    return arr

print(transform([5, 2, 0, 4, 3, 1]))
```

---

## CODE-02: Triple Python Gotcha
**Domain:** Output Prediction
**Type:** exactMatch

What does the following Python code print?

```python
def make_adders():
    adders = []
    for i in range(4):
        def adder(x, cache=[]):
            cache.append(x)
            return i + x + len(cache)
        adders.append(adder)
    return adders

fns = make_adders()
results = [fns[0](10), fns[1](20), fns[2](10), fns[0](5)]
print(results)
```

---

## CODE-03: Tuple Unpacking Evaluation Order
**Domain:** Output Prediction
**Type:** exactMatch

What is the value of `a` after this Python code executes?

```python
a = [0, 1, 2, 3, 4]
a[0], a[a[0]] = 3, 0
print(a)
```

---

## CODE-04: Deceptive Complexity
**Domain:** Complexity Analysis
**Type:** exactMatch

What is the time complexity of the following function, expressed in big-O notation? Also: what does `mystery(100)` return?

```python
def mystery(n):
    count = 0
    for i in range(1, n + 1):
        j = i
        while j % 2 == 0:
            j //= 2
            count += 1
    return count
```

Give both: (1) the big-O complexity and (2) the exact numerical output for n=100.

---

## CODE-05: Lexicographic Topological Sort
**Domain:** Algorithm Analysis
**Type:** exactMatch

Given 6 nodes (labeled 0-5) and directed edges: 5->2, 5->0, 4->0, 4->1, 2->3, 3->1

The following code computes the lexicographically smallest topological ordering using a min-heap. What does it output?

```python
import heapq

def lex_topo_sort(n, edges):
    indegree = [0] * n
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
        indegree[v] += 1
    heap = []
    for i in range(n):
        if indegree[i] == 0:
            heapq.heappush(heap, i)
    result = []
    while heap:
        node = heapq.heappop(heap)
        result.append(node)
        for neighbor in adj[node]:
            indegree[neighbor] -= 1
            if indegree[neighbor] == 0:
                heapq.heappush(heap, neighbor)
    return result

print(lex_topo_sort(6, [(5,2),(5,0),(4,0),(4,1),(2,3),(3,1)]))
```

---

## CODE-06: Generator send() Protocol
**Domain:** Output Prediction
**Type:** exactMatch

What values do the following calls produce? Give the values of r0, r1, r2, r3, and what happens when send(None) is called.

```python
def accumulator():
    total = 0
    while True:
        value = yield total
        if value is None:
            break
        total += value

gen = accumulator()
r0 = next(gen)
r1 = gen.send(10)
r2 = gen.send(20)
r3 = gen.send(5)
print(r0, r1, r2, r3)

try:
    r4 = gen.send(None)
    print(f"returned {r4}")
except StopIteration:
    print("StopIteration raised")
```

---

## CODE-07: LCS Where Greedy Fails
**Domain:** Algorithm Analysis
**Type:** exactMatch (integer)

What is the length of the longest common subsequence of "ABCBDAB" and "BDCABA"?

Give the exact numerical answer. Reason it out using dynamic programming or by enumerating subsequences.

```python
def lcs_length(s1, s2):
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i-1] == s2[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    return dp[m][n]

print(lcs_length("ABCBDAB", "BDCABA"))
```

---

## CODE-08: Derangement Count
**Domain:** Algorithm Design
**Type:** exactMatch (integer)

How many permutations of [1, 2, 3, 4, 5, 6] have NO element in its original position? (Element k is in its "original position" if it occupies index k-1.)

---

## CODE-09: Counting Compositions via Recursion
**Domain:** Output Prediction
**Type:** exactMatch (integer)

What value does `counter` hold after this code executes?

```python
counter = 0

def solve(n):
    global counter
    if n <= 0:
        counter += 1
        return
    for i in range(1, n + 1):
        if i <= 3:
            solve(n - i)

counter = 0
solve(5)
print(counter)
```

---

## CODE-10: defaultdict Auto-Vivification Chain
**Domain:** Output Prediction
**Type:** exactMatch

What four values does this code print (as a tuple)?

```python
from collections import defaultdict

def build_and_query():
    graph = defaultdict(list)
    edges = [(0,1), (1,2), (2,0), (0,3)]
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)

    keys_before = len(graph)
    _ = graph[99]
    keys_after = len(graph)

    check = 42 in graph
    keys_final = len(graph)

    return keys_before, keys_after, check, keys_final

print(build_and_query())
```
