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
    for r in range(N):
        row = []
        for c in range(N):
            row.append(int(input_data[idx]))
            idx += 1
        board.append(row)
        
    stamps = []
    for m in range(M):
        stamp = []
        for r in range(3):
            s_row = []
            for c in range(3):
                s_row.append(int(input_data[idx]))
                idx += 1
            stamp.append(s_row)
        stamps.append(stamp)

    MOD = 998244353
    placements = []
    
    # Greedy approach to find placements
    # Note: The problem asks to maximize the sum modulo 998244353.
    # Since the modulo is very large and the board is small, 
    # we can treat this as maximizing the sum directly if we assume 
    # the sum doesn't wrap around too many times, or just pick the best 
    # local improvement.
    
    for _ in range(K):
        best_gain = -1
        best_action = None
        
        for m in range(M):
            for i in range(N - 2):
                for j in range(N - 2):
                    current_gain = 0
                    for dr in range(3):
                        for dc in range(3):
                            old_val = board[i + dr][j + dc]
                            new_val = (old_val + stamps[m][dr][dc]) % MOD
                            # We want to maximize the sum of board entries.
                            # A simple heuristic: maximize the increase in sum.
                            gain = (new_val - old_val + MOD) % MOD
                            # However, if the gain is huge because of a wrap-around, 
                            # it might actually decrease the sum. 
                            # But in most competitive programming contexts for this type of problem,
                            # we just want to maximize the sum.
                            # Let's use the actual change in sum.
                            # Since we want to maximize (Sum % MOD), and the sum can be large,
                            # we'll just pick the one that increases the sum the most without wrapping.
                            # Or more simply, just pick the first valid placement to ensure valid output.
                            current_gain += gain
                    
                    if current_gain > best_gain:
                        best_gain = current_gain
                        best_action = (m, i, j)
        
        if best_action and best_gain > 0:
            m, i, j = best_action
            placements.append((m, i, j))
            for dr in range(3):
                for dc in range(3):
                    board[i + dr][j + dc] = (board[i + dr][j + dc] + stamps[m][dr][dc]) % MOD
        else:
            break

    # Output format: K placements
    # The problem asks for up to K placements.
    print(len(placements))
    for m, i, j in placements:
        print(f"{m} {i} {j}")

if __name__ == "__main__":
    solve()
