import sys

def main():
    input_data = sys.stdin.read().split()
    idx = 0
    N = int(input_data[idx]); idx += 1
    M = int(input_data[idx]); idx += 1
    K = int(input_data[idx]); idx += 1

    MOD = 998244353

    board = [[0]*N for _ in range(N)]
    for i in range(N):
        for j in range(N):
            board[i][j] = int(input_data[idx]); idx += 1

    stamps = []
    for m in range(M):
        stamp = [[0]*3 for _ in range(3)]
        for i in range(3):
            for j in range(3):
                stamp[i][j] = int(input_data[idx]); idx += 1
        stamps.append(stamp)

    operations = []

    for step in range(K):
        best_gain = -1
        best_op = None
        for m in range(M):
            for r in range(N - 2):
                for c in range(N - 2):
                    gain = 0
                    for di in range(3):
                        for dj in range(3):
                            old_val = board[r + di][c + dj]
                            new_val = (old_val + stamps[m][di][dj]) % MOD
                            gain += new_val - old_val
                    if gain > best_gain:
                        best_gain = gain
                        best_op = (m, r, c)
        if best_gain <= 0:
            break
        m, r, c = best_op
        for di in range(3):
            for dj in range(3):
                board[r + di][c + dj] = (board[r + di][c + dj] + stamps[m][di][dj]) % MOD
        operations.append((m + 1, r + 1, c + 1))

    print(len(operations))
    for op in operations:
        print(op[0], op[1], op[2])

main()
