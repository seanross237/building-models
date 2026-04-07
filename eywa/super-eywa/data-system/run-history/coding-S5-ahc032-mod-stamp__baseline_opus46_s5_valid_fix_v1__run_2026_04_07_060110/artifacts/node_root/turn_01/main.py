import sys

def main():
    input_data = sys.stdin.read().split()
    idx = 0
    N = int(input_data[idx]); idx += 1
    M = int(input_data[idx]); idx += 1
    K = int(input_data[idx]); idx += 1

    MOD = 998244353

    board = []
    for i in range(N):
        row = []
        for j in range(N):
            row.append(int(input_data[idx])); idx += 1
        board.append(row)

    stamps = []
    for m in range(M):
        stamp = []
        for r in range(3):
            row = []
            for c in range(3):
                row.append(int(input_data[idx])); idx += 1
            stamp.append(row)
        stamps.append(stamp)

    placements = []

    for _ in range(K):
        best_gain = -1
        best_m = -1
        best_i = -1
        best_j = -1

        for m in range(M):
            stamp = stamps[m]
            for i in range(N - 2):
                for j in range(N - 2):
                    gain = 0
                    for r in range(3):
                        for c in range(3):
                            old_val = board[i + r][j + c]
                            new_val = (old_val + stamp[r][c]) % MOD
                            gain += new_val - old_val
                    if gain > best_gain:
                        best_gain = gain
                        best_m = m
                        best_i = i
                        best_j = j

        if best_gain <= 0:
            break

        stamp = stamps[best_m]
        for r in range(3):
            for c in range(3):
                board[best_i + r][best_j + c] = (board[best_i + r][best_j + c] + stamp[r][c]) % MOD
        placements.append((best_m + 1, best_i + 1, best_j + 1))

    print(len(placements))
    for m, i, j in placements:
        print(m, i, j)

main()
