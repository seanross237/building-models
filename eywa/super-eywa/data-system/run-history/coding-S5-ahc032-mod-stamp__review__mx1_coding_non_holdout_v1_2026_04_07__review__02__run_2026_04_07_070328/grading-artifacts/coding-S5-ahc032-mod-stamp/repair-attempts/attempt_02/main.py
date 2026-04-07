import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    ptr = 0
    try:
        N = int(input_data[ptr]); ptr += 1
        M = int(input_data[ptr]); ptr += 1
        K = int(input_data[ptr]); ptr += 1
        
        MOD = 998244353
        
        board = []
        for i in range(N):
            row = []
            for j in range(N):
                row.append(int(input_data[ptr]))
                ptr += 1
            board.append(row)
            
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
    except (IndexError, ValueError):
        return

    placements = []
    
    # Greedy approach to pick up to K placements.
    # The scorer error 'Out of range' suggests the indices m, r, or c were invalid.
    # In the original code, r and c were in range(N-2), which is correct for 3x3 on NxN.
    # However, the greedy loop might have been picking invalid indices or the input reading failed.
    # We will implement a safer greedy that respects the bounds strictly.
    
    for _ in range(K):
        best_gain = -1
        best_move = None
        
        for m in range(M):
            for r in range(N - 2):
                for c in range(N - 2):
                    current_gain = 0
                    for dr in range(3):
                        for dc in range(3):
                            old_val = board[r + dr][c + dc]
                            new_val = (old_val + stamps[m][dr][dc]) % MOD
                            # Heuristic: maximize the increase in value
                            # Since we want to maximize sum % MOD, and MOD is huge,
                            # we treat it as maximizing the sum.
                            current_gain += (new_val - old_val)
                    
                    if current_gain > best_gain:
                        best_gain = current_gain
                        best_move = (m, r, c)
        
        if best_move is not None and best_gain > 0:
            m, r, c = best_move
            placements.append((m, r, c))
            for dr in range(3):
                for dc in range(3):
                    board[r + dr][c + dc] = (board[r + dr][c + dc] + stamps[m][dr][dc]) % MOD
        else:
            break

    for m, r, c in placements:
        print(f"{m} {r} {c}")

if __name__ == '__main__':
    solve()
