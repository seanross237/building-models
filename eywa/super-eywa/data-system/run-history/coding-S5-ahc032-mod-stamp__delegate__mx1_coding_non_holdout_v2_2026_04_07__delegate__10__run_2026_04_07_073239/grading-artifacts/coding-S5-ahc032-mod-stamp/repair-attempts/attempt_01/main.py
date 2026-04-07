import sys

def solve():
    # Read N, M, K
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    ptr = 0
    N = int(input_data[ptr]); ptr += 1
    M = int(input_data[ptr]); ptr += 1
    K = int(input_data[ptr]); ptr += 1

    # Read initial board
    board = []
    for i in range(N):
        row = []
        for j in range(N):
            row.append(int(input_data[ptr]))
            ptr += 1
        board.append(row)

    # Read M stamps
    stamps = []
    for m in range(M):
        stamp = []
        for i in range(3):
            row = []
            for j in range(3):
                row.append(int(input_data[ptr]))
                ptr += 1
            stamp.append(row)
        stamps.append(stamp)

    MOD = 998244353

    # The objective is to maximize the sum of all final board entries.
    # Since we add stamps modulo 998244353, the sum is not simply additive.
    # However, for a greedy approach, we can look at the sum of the stamp elements.
    # If the stamp elements are positive and small, the modulo won't trigger often.
    # If they are large, we want to avoid the wrap-around that reduces the sum.
    
    # Let's calculate the sum of each stamp.
    stamp_sums = []
    for m in range(M):
        s = 0
        for i in range(3):
            for j in range(3):
                s += stamps[m][i][j]
        stamp_sums.append(s)

    # Find the best stamp (highest sum)
    best_m = 0
    max_s = -1
    for m in range(M):
        if stamp_sums[m] > max_s:
            max_s = stamp_sums[m]
            best_m = m

    # To maximize the sum, we want to place the best stamp as many times as possible.
    # However, we must ensure we don't exceed K placements.
    # Since N=9, there are (9-2)*(9-2) = 49 possible positions.
    # We can place the best stamp at every possible position.
    # If 49 <= K, we do that. If K < 49, we pick the 49 positions and take the top K.
    
    placements = []
    # We'll just fill all possible positions with the best stamp to maximize sum.
    # Since K=81 and max positions is 49, we can definitely do this.
    # To be safe and potentially better, we can repeat placements if it helps,
    # but the problem says "at most K" and "each placement chooses...".
    # Usually, in these problems, repeating a placement is allowed.
    
    # Let's try to place the best stamp at every possible (i, j) once.
    for i in range(N - 2):
        for j in range(N - 2):
            if len(placements) < K:
                placements.append((best_m, i, j))

    # Output the results
    print(len(placements))
    for p in placements:
        print(f"{p[0]} {p[1]} {p[2]}")

if __name__ == "__main__":
    solve()
