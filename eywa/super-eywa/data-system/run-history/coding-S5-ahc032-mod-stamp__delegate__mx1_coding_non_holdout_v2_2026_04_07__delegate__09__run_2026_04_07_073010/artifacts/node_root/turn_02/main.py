import sys
import random
import time

def solve():
    # Read N, M, K
    try:
        line1 = sys.stdin.readline().split()
        if not line1: return
        N, M, K = map(int, line1)
    except EOFError:
        return

    MOD = 998244353

    # Read initial board
    board = []
    for _ in range(N):
        board.append(list(map(int, sys.stdin.readline().split())))

    # Read M stamps
    stamps = []
    for _ in range(M):
        stamp = []
        for _ in range(3):
            stamp.append(list(map(int, sys.stdin.readline().split())))
        stamps.append(stamp)

    # Helper to calculate score change
    # Since we want to maximize sum(board), and board is updated modulo MOD,
    # we must track the actual values. However, the problem says "The chosen 3x3 stamp is added to the board modulo 998244353".
    # This implies: board[i][j] = (board[i][j] + stamp[di][dj]) % MOD.
    
    def get_score_delta(current_board, stamp_idx, r, c):
        delta = 0
        stamp = stamps[stamp_idx]
        for dr in range(3):
            for dc in range(3):
                old_val = current_board[r + dr][c + dc]
                new_val = (old_val + stamp[dr][dc]) % MOD
                delta += (new_val - old_val)
        return delta

    def apply_stamp(current_board, stamp_idx, r, c):
        stamp = stamps[stamp_idx]
        for dr in range(3):
            for dc in range(3):
                current_board[r + dr][c + dc] = (current_board[r + dr][c + dc] + stamp[dr][dc]) % MOD

    def remove_stamp(current_board, stamp_idx, r, c):
        stamp = stamps[stamp_idx]
        for dr in range(3):
            for dc in range(3):
                # To reverse (a + b) % MOD = c, we do (c - b) % MOD
                current_board[r + dr][c + dc] = (current_board[r + dr][c + dc] - stamp[dr][dc]) % MOD

    # Greedy Phase
    current_board = [row[:] for row in board]
    placements = [] # list of (m, i, j)
    
    # We have K placements allowed.