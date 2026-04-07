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
            srow = []
            for c in range(3):
                srow.append(int(input_data[idx])); idx += 1
            stamp.append(srow)
        stamps.append(stamp)

    placements = []

    for step in range(K):
        best_gain = -1
        best_m = -1
        best_i = -1
        best_j = -1
        for m in range(M):
            for i in range(N - 2):
                for j in range(N - 2):
                    gain = 0
                    for dr in range(3):
                        for dc in range(3):
                            old_val = board[i + dr][j + dc]
                            new_val = (old_val + stamps[m][dr][dc]) % MOD
                            gain += new_val - old_val
                    if gain > best_gain:
                        best_gain = gain
                        best_m = m
                        best_i = i
                        best_j = j
        if best_gain <= 0:
            break
        placements.append((best_m, best_i, best_j))
        for dr in range(3):
            for dc in range(3):
                board[best_i + dr][best_j + dc] = (board[best_i + dr][best_j + dc] + stamps[best_m][dr][dc]) % MOD

    print(len(placements))
    for m, i, j in placements:
        print(m, i, j)

main()
