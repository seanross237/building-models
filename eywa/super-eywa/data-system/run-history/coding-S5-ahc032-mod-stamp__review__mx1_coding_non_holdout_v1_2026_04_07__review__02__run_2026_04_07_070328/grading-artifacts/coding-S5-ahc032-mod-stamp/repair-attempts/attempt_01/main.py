import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    ptr = 0
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

    placements = []
    
    # Greedy approach: pick the best stamp/position that maximizes the sum of board entries
    # Note: The score is the sum of final board entries.
    # Since we add modulo 998244353, the gain can be negative if a value wraps around.
    # However, the problem asks for the sum of final entries.
    
    for _ in range(K):
        best_gain = -float('inf')
        best_move = None
        
        for m in range(M):
            for r in range(N - 2):
                for c in range(N - 2):
                    current_gain = 0
                    for dr in range(3):
                        for dc in range(3):
                            old_val = board[r + dr][c + dc]
                            new_val = (old_val + stamps[m][dr][dc]) % MOD
                            # The change in the total sum is (new_val - old_val)
                            current_gain += (new_val - old_val)
                    
                    if current_gain > best_gain:
                        best_gain = current_gain
                        best_move = (m, r, c)
        
        # If the best move doesn't increase the sum, we stop (or just pick it if we must)
        # But we can pick at most K, so we only pick if it's beneficial.
        if best_move and best_gain > 0:
            m, r, c = best_move
            placements.append((m, r, c))
            for dr in range(3):
                for dc in range(3):
                    board[r + dr][c + dc] = (board[r + dr][c + dc] + stamps[m][dr][dc]) % MOD
        else:
            break

    # Output format:
    # L
    # m i j (L lines)
    print(len(placements))
    for m, r, c in placements:
        print(f"{m} {r} {c}")

if __name__ == "__main__":
    solve()
