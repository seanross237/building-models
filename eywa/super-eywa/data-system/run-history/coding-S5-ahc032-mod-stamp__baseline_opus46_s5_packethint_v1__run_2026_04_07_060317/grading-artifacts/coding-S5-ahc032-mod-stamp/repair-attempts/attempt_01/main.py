import sys

def main():
    MOD = 998244353
    data = sys.stdin.read().split()
    idx = 0
    N = int(data[idx]); idx += 1
    M = int(data[idx]); idx += 1
    K = int(data[idx]); idx += 1

    # Read the initial board (N x N = 9 x 9)
    board = [[0]*N for _ in range(N)]
    for r in range(N):
        for c in range(N):
            board[r][c] = int(data[idx]); idx += 1

    # Read M stamps, each 3x3
    stamps = []
    for s in range(M):
        stamp = []
        for r in range(3):
            row = []
            for c in range(3):
                row.append(int(data[idx])); idx += 1
            stamp.append(row)
        stamps.append(stamp)

    placements = []

    for step in range(K):
        best_gain = 0
        best_s = -1
        best_i = 0
        best_j = 0

        for s in range(M):
            for i in range(N - 2):
                for j in range(N - 2):
                    gain = 0
                    for dr in range(3):
                        for dc in range(3):
                            old_val = board[i + dr][j + dc]
                            new_val = (old_val + stamps[s][dr][dc]) % MOD
                            gain += (new_val - old_val)
                    if gain > best_gain:
                        best_gain = gain
                        best_s = s
                        best_i = i
                        best_j = j

        if best_s == -1:
            # No positive gain found, try to find least negative or break
            # Actually let's try: maybe adding stamps that cause wrap-around is bad
            # Let's also consider: even if gain is 0 or negative, we stop
            break

        # Apply the best placement
        placements.append((best_s, best_i, best_j))
        for dr in range(3):
            for dc in range(3):
                board[best_i + dr][best_j + dc] = (board[best_i + dr][best_j + dc] + stamps[best_s][dr][dc]) % MOD

    print(len(placements))
    for (s, i, j) in placements:
        print(s, i, j)

if __name__ == '__main__':
    main()
