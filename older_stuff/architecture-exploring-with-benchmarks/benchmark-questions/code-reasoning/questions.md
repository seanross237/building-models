# Code Reasoning Benchmark

10 algorithmic/coding problems with deterministic, verifiable answers.
Tests code reasoning and algorithmic thinking -- not implementation ability.
All answers verified by execution.

Difficulty: medium-hard. Designed to penalize models that shortcut reasoning.
Each problem has at least one plausible-but-wrong answer that a model will reach
if it makes a common reasoning error.

---

## CODE-01: Self-Referential Array Mutation
Category: output-prediction
Answer: `[1, 0, 1, 3, 3, 0]`

What does the following Python code return?

```python
def transform(arr):
    n = len(arr)
    for i in range(n):
        arr[i] = arr[arr[i] % n]
    return arr

print(transform([5, 2, 0, 4, 3, 1]))
```

**Why it's hard:** Each write mutates the array in-place, so subsequent reads see
already-modified values. Models that trace using the original array will get:
`[1, 0, 5, 3, 4, 2]` (wrong). The correct trace must update step-by-step:

- i=0: arr[0] = arr[5%6] = arr[5] = 1.  arr is now [1, 2, 0, 4, 3, 1]
- i=1: arr[1] = arr[2%6] = arr[2] = 0.  arr is now [1, 0, 0, 4, 3, 1]
- i=2: arr[2] = arr[0%6] = arr[0] = 1.  arr is now [1, 0, 1, 4, 3, 1]
- i=3: arr[3] = arr[4%6] = arr[4] = 3.  arr is now [1, 0, 1, 3, 3, 1]
- i=4: arr[4] = arr[3%6] = arr[3] = 3.  arr is now [1, 0, 1, 3, 3, 1]
- i=5: arr[5] = arr[1%6] = arr[1] = 0.  arr is now [1, 0, 1, 3, 3, 0]

---

## CODE-02: Triple Python Gotcha
Category: output-prediction
Answer: `[14, 24, 14, 10]`

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

**Why it's hard:** Three interacting Python gotchas determine the answer:

1. **Closure over loop variable:** All four `adder` functions close over the same
   variable `i`. After the loop, `i = 3`. So every call uses `i = 3`, not the
   value of `i` at definition time. (If you assume `i` varies: wrong answer `[11, 21, 12, 8]`)

2. **Mutable default argument persistence:** Each function created in the loop gets
   its own `cache=[]` default (because each `def` creates a new function object).
   But that cache persists across calls to the SAME function. So `fns[0](5)` sees
   cache already containing `[10]` from the earlier `fns[0](10)` call.
   (If you assume cache is shared across ALL functions: wrong answer `[14, 25, 16, 12]`)

3. **Cache does NOT reset between calls:** The mutable default `[]` is created once
   per function, not once per call. So `fns[0]`'s second call has `len(cache) = 2`.
   (If you assume cache resets: wrong answer `[14, 24, 14, 9]`)

Trace:
- `fns[0](10)`: i=3, x=10, cache was [], append(10) -> cache=[10], len=1. Return 3+10+1 = 14
- `fns[1](20)`: i=3, x=20, cache was [], append(20) -> cache=[20], len=1. Return 3+20+1 = 24
- `fns[2](10)`: i=3, x=10, cache was [], append(10) -> cache=[10], len=1. Return 3+10+1 = 14
- `fns[0](5)`:  i=3, x=5,  cache was [10], append(5) -> cache=[10,5], len=2. Return 3+5+2 = 10

---

## CODE-03: Tuple Unpacking Evaluation Order
Category: output-prediction
Answer: `[3, 1, 2, 0, 4]`

What is the value of `a` after this Python code executes?

```python
a = [0, 1, 2, 3, 4]
a[0], a[a[0]] = 3, 0
print(a)
```

**Why it's hard:** Python evaluates the RHS fully, then assigns to LHS targets
left-to-right. The critical insight is that `a[0]` is assigned FIRST, which
changes what `a[a[0]]` refers to.

- RHS evaluated: `(3, 0)`
- Assign `a[0] = 3`. Now a = [3, 1, 2, 3, 4]
- Assign `a[a[0]]` = `a[3]` = 0. Now a = [3, 1, 2, 0, 4]

Common wrong answer: `[3, 1, 2, 3, 4]` (if you think `a[a[0]]` uses the
original `a[0]=0`, writing to `a[0]` again) or `[0, 1, 2, 3, 4]` (if you think
both writes use original indices).

Bonus: reversing the LHS targets produces a completely different result.
`b = [0,1,2,3,4]; b[b[0]], b[0] = 3, 0` gives `b = [0, 1, 2, 3, 4]` (unchanged!).

---

## CODE-04: Deceptive Complexity
Category: complexity-analysis
Answer: `O(n)`

What is the time complexity of the following function, expressed in big-O notation?

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

Also: what does `mystery(100)` return?
Exact numerical answer: `97`

**Why it's hard:** The nested while loop makes this LOOK like O(n log n). But the
total inner work across all iterations of `i` is bounded by a geometric series:
- n/2 values of i are divisible by 2 (contribute >= 1 inner step)
- n/4 values are divisible by 4 (contribute >= 1 more)
- n/8 values are divisible by 8 (contribute >= 1 more)
- Total inner steps = n/2 + n/4 + n/8 + ... < n

So the total work is O(n) + O(n) = O(n). The inner loop contributes O(n) total,
not O(n log n). This is the same argument used in amortized analysis of binary
counting.

For n=100: sum = floor(100/2) + floor(100/4) + floor(100/8) + floor(100/16) +
floor(100/32) + floor(100/64) = 50 + 25 + 12 + 6 + 3 + 1 = 97.

---

## CODE-05: Lexicographic Topological Sort
Category: algorithm-analysis
Answer: `[4, 5, 0, 2, 3, 1]`

Given 6 nodes (labeled 0-5) and directed edges:
`5->2, 5->0, 4->0, 4->1, 2->3, 3->1`

The following code computes the lexicographically smallest topological ordering
using a min-heap. What does it output?

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

**Why it's hard:** The lexicographically smallest topological sort is NOT the same
as sorting the nodes and respecting edges. The min-heap greedily picks the smallest
available node at each step, but which nodes become available depends on the
processing order. Must trace the heap state carefully:

- Indegrees: [2, 2, 1, 1, 0, 0]. Heap starts: [4, 5]
- Pop 4. Process 4->0 (indeg 2->1), 4->1 (indeg 2->1). Heap: [5]
- Pop 5. Process 5->2 (indeg 1->0, push 2), 5->0 (indeg 1->0, push 0). Heap: [0, 2]
- Pop 0. No outgoing edges from 0. Heap: [2]
- Pop 2. Process 2->3 (indeg 1->0, push 3). Heap: [3]
- Pop 3. Process 3->1 (indeg 1->0, push 1). Heap: [1]
- Pop 1. Result: [4, 5, 0, 2, 3, 1]

Common wrong answer: `[4, 5, 2, 0, 3, 1]` (if you process 5's neighbors in edge
order and don't realize the heap reorders them).

---

## CODE-06: Generator send() Protocol
Category: output-prediction
Answer: `0, 10, 30, 35, StopIteration`

What values do the following calls produce?

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

Give the values of r0, r1, r2, r3, and what happens when send(None) is called.

**Why it's hard:** Requires understanding the full generator protocol:

- `next(gen)` advances to the first `yield`, which yields `total=0`. r0 = 0
- `gen.send(10)`: resumes, `value=10`, `total=0+10=10`, loops to `yield 10`. r1 = 10
- `gen.send(20)`: resumes, `value=20`, `total=10+20=30`, loops to `yield 30`. r2 = 30
- `gen.send(5)`: resumes, `value=5`, `total=30+5=35`, loops to `yield 35`. r3 = 35
- `gen.send(None)`: resumes, `value=None`, hits `break`, generator returns -> StopIteration

Common errors: thinking `next(gen)` returns None, or thinking `send()` resumes
AFTER the yield rather than AT the yield, or thinking `send(None)` returns 35.

---

## CODE-07: LCS Where Greedy Fails
Category: algorithm-analysis
Answer: `4`

What is the length of the longest common subsequence of `"ABCBDAB"` and `"BDCABA"`?

Give the exact numerical answer. You may not run the code -- reason it out using
dynamic programming or by enumerating subsequences.

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

**Why it's hard:** A greedy approach (match each character to its earliest
occurrence in the other string) gives the wrong answer. For instance, greedily
matching `B` first in `"BDCABA"` uses position 0, then trying to match `D` at
position 2, `A` at position 3, `B` at position 4 gives LCS = "BDAB" = 4.
That happens to be correct here, but the reasoning path is fragile.

The full DP table must be traced (7x6 = 42 cells) to be sure. One valid LCS
is "BCBA" (B at positions 0/0, C at positions 2/2, B at positions 3/4, A at
positions 6/5). Another is "BDAB".

---

## CODE-08: Derangement Count
Category: algorithm-design
Answer: `265`

How many permutations of [1, 2, 3, 4, 5, 6] have NO element in its original
position? (Element `k` is in its "original position" if it occupies index `k-1`.)

This is the derangement number D(6).

**Why it's hard:** There are multiple valid approaches, each with its own pitfall.

**Approach 1 — Inclusion-exclusion formula:** D(n) = n! * sum_{k=0}^{n} (-1)^k / k!

D(6) = 720 * (1 - 1 + 1/2 - 1/6 + 1/24 - 1/120 + 1/720)
     = 720 - 720 + 360 - 120 + 30 - 6 + 1
     = 265

The trap: rounding errors if you use decimals instead of exact fractions.

**Approach 2 — Recurrence:** D(n) = (n-1) * (D(n-1) + D(n-2))

- D(0) = 1, D(1) = 0
- D(2) = 1 * (0 + 1) = 1
- D(3) = 2 * (1 + 0) = 2
- D(4) = 3 * (2 + 1) = 9
- D(5) = 4 * (9 + 2) = 44
- D(6) = 5 * (44 + 9) = 265

The trap: if you confuse the derangement recurrence with the Fibonacci-style
recurrence (D(n) = D(n-1) + D(n-2)) or use wrong base values (e.g., D(0) = 0
instead of 1), you get wildly different answers. A common wrong answer is 264
(from an off-by-one in the inclusion-exclusion sum).

**Approach 3 — Alternative recurrence:** D(n) = n * D(n-1) + (-1)^n

- D(2) = 2*0 + 1 = 1
- D(3) = 3*1 - 1 = 2
- D(4) = 4*2 + 1 = 9
- D(5) = 5*9 - 1 = 44
- D(6) = 6*44 + 1 = 265

---

## CODE-09: Counting Compositions via Recursion
Category: output-prediction
Answer: `13`

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

**Why it's hard:** This counts ordered compositions of 5 using parts in {1, 2, 3},
but the code structure obscures this. The `for i in range(1, n+1)` iterates
beyond 3 but the `if i <= 3` guard silently skips those iterations. A model might
mistakenly think the loop always runs n times (overcounting) or might confuse
ordered compositions with unordered partitions (p(5) = 7, wrong).

The recursion is equivalent to the tribonacci-like recurrence f(n) = f(n-1) + f(n-2) + f(n-3):
- f(0) = 1 (base case: n<=0)
- f(1) = f(0) = 1
- f(2) = f(1) + f(0) = 2
- f(3) = f(2) + f(1) + f(0) = 4
- f(4) = f(3) + f(2) + f(1) = 7
- f(5) = f(4) + f(3) + f(2) = 13

Also: the base case triggers when `n <= 0`, not `n == 0`. When `n = 0`,
`range(1, 1)` is empty so the loop doesn't execute, but we already handled
it. When `n < 0`... can that happen? If `i > n` and `i <= 3`, yes. For example,
`solve(1)` calls `solve(1-2) = solve(-1)` and `solve(1-3) = solve(-2)`. But
those hit `n <= 0` immediately, each incrementing counter once. This means
`solve(1)` increments counter 3 times? No: `solve(1)` iterates i=1,2,3 since
`range(1,2)` only yields i=1, and 1<=3, so only `solve(0)` is called. Wait:
`range(1, n+1)` where n=1 gives `range(1, 2)` = [1]. So only i=1.
solve(1) -> solve(0) -> counter += 1. Just once. f(1) = 1. Correct.

---

## CODE-10: defaultdict Auto-Vivification Chain
Category: output-prediction
Answer: `4, 5, False, 5`

What four values does this code print?

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

**Why it's hard:** Three distinct defaultdict behaviors interact:

1. **Which keys exist after building the graph?** Edges (0,1), (1,2), (2,0), (0,3)
   touch nodes 0, 1, 2, 3. So `keys_before = 4`. (If you count edges instead: wrong.)

2. **Accessing a missing key creates it.** `graph[99]` returns `[]` (the default)
   AND inserts key 99. So `keys_after = 5`. This is the core defaultdict trap --
   unlike a regular dict, mere subscription (`d[key]`) creates the key if missing.

3. **`in` does NOT create the key.** `42 in graph` returns False and does NOT
   insert 42. So `keys_final = 5`, not 6. The `__contains__` method does not
   trigger `__missing__`.

Common wrong answers:
- `(4, 4, False, 4)` if you don't know about auto-vivification
- `(4, 5, False, 6)` if you think `in` also creates keys
- `(8, 9, False, 9)` if you count edge endpoints instead of unique nodes

---

# Summary Table

| ID | Title | Category | Answer | Primary Trap |
|----|-------|----------|--------|-------------|
| CODE-01 | Self-Referential Array Mutation | output-prediction | `[1, 0, 1, 3, 3, 0]` | In-place mutation changes subsequent reads |
| CODE-02 | Triple Python Gotcha | output-prediction | `[14, 24, 14, 10]` | Closure + mutable default + persistence |
| CODE-03 | Tuple Unpacking Order | output-prediction | `[3, 1, 2, 0, 4]` | LHS targets evaluated left-to-right after RHS |
| CODE-04 | Deceptive Complexity | complexity-analysis | `O(n)`, exact: `97` | Looks O(n log n) but amortizes to O(n) |
| CODE-05 | Lexicographic Topo Sort | algorithm-analysis | `[4, 5, 0, 2, 3, 1]` | Heap ordering vs. edge processing order |
| CODE-06 | Generator send() Protocol | output-prediction | `0, 10, 30, 35, StopIteration` | send() resumes at yield, not after |
| CODE-07 | LCS Where Greedy Fails | algorithm-analysis | `4` | Greedy matching gives wrong reasoning path |
| CODE-08 | Derangement Count | algorithm-design | `265` | Multiple recurrences, easy to use wrong one |
| CODE-09 | Counting Compositions | output-prediction | `13` | Ordered compositions != partitions, guard clause |
| CODE-10 | defaultdict Auto-Vivification | output-prediction | `(4, 5, False, 5)` | Subscription creates keys, `in` does not |
