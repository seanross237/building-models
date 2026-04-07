import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    idx = 0
    N = int(input_data[idx]); idx += 1
    M = int(input_data[idx]); idx += 1
    K = int(input_data[idx]); idx += 1
    
    MOD = 998244353
    
    board = []
    for i in range(N):
        row = []
        for j in range(N):
            row.append(int(input_data[idx]))
            idx += 1
        board.append(row)
        
    stamps = []
    for m in range(M):
        stamp = []
        for r in range(3):
            row = []
            for c in range(3):
                row.append(int(input_data[idx]))
                idx += 1
            stamp.append(row)
        stamps.append(stamp)

    # The problem asks for up to K placements. 
    # The output format for this type of problem is usually the number of placements followed by the placements.
    # However, the scorer error 'Out of range' suggests the contestant printed the total sum instead of the placements.
    # Based on typical AHC/AHC-style problems, we output the number of placements and then each placement (m, r, c).
    
    placements = []
    # Greedy approach to find placements
    # Note: We must ensure we don't exceed K.
    for _ in range(K):
        best_gain = -1
        best_move = None
        
        for m in range(M):
            for i in range(N - 2):
                for j in range(N - 2):
                    current_gain = 0
                    for dr in range(3):
                        for dc in range(3):
                            old_val = board[i + dr][j + dc]
                            new_val = (old_val + stamps[m][dr][dc]) % MOD
                            # The gain is the change in the sum modulo 998244353
                            # But the problem asks to maximize the sum of board entries modulo 998244353.
                            # This usually means the final sum is taken modulo 998244353.
                            # However, the scorer error shows the contestant printed a huge number.
                            # Let's assume the goal is to maximize (Sum of board[i][j]) % MOD.
                            # Since we can't easily predict the modulo behavior, a simple greedy on the raw sum increase is a baseline.
                            current_gain += (new_val - old_val)
                    
                    if current_gain > best_gain:
                        best_gain = current_gain
                        best_move = (m, i, j)
        
        if best_move and best_gain > 0:
            m, i, j = best_move
            placements.append((m, i, j))
            for dr in range(3):
                for dc in range(3):
                    board[i + dr][j + dc] = (board[i + dr][j + dc] + stamps[m][dr][dc]) % MOD
        else:
            break

    # Output format: Number of placements, then each placement (m, r, c)
    print(len(placements))
    for m, r, c in placements:
        print(f"{m} {r} {c}")

if __name__ == '__main__':
    solve()
