import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    N = int(input_data[0])
    M = int(input_data[1])
    K = int(input_data[2])
    idx = 3
    board = []
    for _ in range(N):
        row = []
        for _ in range(N):
            row.append(int(input_data[idx]))
            idx += 1
        board.append(row)
    stamps = []
    for _ in range(M):
        stamp = []
        for _ in range(3):
            s_row = []
            for _ in range(3):
                s_row.append(int(input_data[idx]))
                idx += 1
            stamp.append(s_row)
        stamps.append(stamp)
    MOD = 998244353
    current_board = [row[:] for row in board]
    for _ in range(K):
        best_gain = -1
        best_move = None
        for m_idx in range(M):
            stamp = stamps[m_idx]
            for r in range(N - 2):
                for c in range(N - 2):
                    gain = 0
                    for dr in range(3):
                        for dc in range(3):
                            val_to_add = stamp[dr][dc]
                            if val_to_add != 0:
                                current_val = current_board[r+dr][c+dc]
                                new_val = (current_val + val_to_add) % MOD
                                gain += (new_val - current_val)
                    if gain > best_gain:
                        best_gain = gain
                        best_move = (m_idx, r, c)
        if best_move and best_gain > 0:
            m_idx, r, c = best_move
            for dr in range(3):
                for dc in range(3):
                    current_board[r+dr][c+dc] = (current_board[r+dr][c+dc] + stamps[m_idx][dr][dc]) % MOD
        else:
            break
    total_sum = sum(sum(row) for row in current_board) % MOD
    print(total_sum)

solve()