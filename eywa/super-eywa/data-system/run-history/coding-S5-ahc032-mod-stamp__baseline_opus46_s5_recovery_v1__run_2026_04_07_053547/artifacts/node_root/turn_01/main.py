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
    for s in range(M):
        stamp = [[0]*3 for _ in range(3)]
        for i in range(3):
            for j in range(3):
                stamp[i][j] = int(input_data[idx]); idx += 1
        stamps.append(stamp)

    results = []
    for _ in range(K):
        best_gain = -1
        best_choice = None
        for s_idx, stamp in enumerate(stamps):
            for r in range(N - 2):
                for c in range(N - 2):
                    gain = 0
                    for di in range(3):
                        for dj in range(3):
                            old_val = board[r+di][c+dj]
                            new_val = (old_val + stamp[di][dj]) % MOD
                            gain += new_val - old_val
                    if gain > best_gain:
                        best_gain = gain
                        best_choice = (s_idx, r, c)
        if best_choice is None or best_gain <= 0:
            break
        s_idx, r, c = best_choice
        stamp = stamps[s_idx]
        for di in range(3):
            for dj in range(3):
                board[r+di][c+dj] = (board[r+di][c+dj] + stamp[di][dj]) % MOD
        results.append(best_choice)

    total = 0
    for i in range(N):
        for j in range(N):
            total += board[i][j]
    print(total % MOD)
    print(len(results))
    for s_idx, r, c in results:
        print(s_idx, r, c)

main()
