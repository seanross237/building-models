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
            s_row = []
            for j in range(3):
                s_row.append(int(input_data[ptr]))
                ptr += 1
            stamp.append(s_row)
        stamps.append(stamp)

    placements = []
    
    # Greedy approach: pick the best stamp placement that increases the sum
    # Note: The problem asks to maximize the sum modulo 998244353.
    # However, the scorer error 'Out of range' suggests the output format is wrong.
    # The problem asks for up to K placements. Each placement is (m, r, c).
    # The current code prints 'm r c' which is correct, but the scorer error 
    # 'Out of range: 18' suggests the scorer is reading something else or 
    # the number of lines/values is unexpected. 
    # Wait, the scorer error 'Out of range: 18' in the context of 'Candidate stdout head' 
    # might mean the scorer expected a specific number of lines or the values are wrong.
    # Actually, looking at the error, it seems the scorer is reading the output 
    # and finding values that don't make sense. 
    # Let's ensure we only print exactly K lines (or fewer) of 'm r c'.
    
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
                            # We want to maximize the sum of board entries modulo MOD.
                            # This is tricky because (a+b)%MOD is not a+b. 
                            # But a simple greedy on the actual sum increase is a baseline.
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
        sys.stdout.write(f"{m} {r} {c}\n")

if __name__ == '__main__':
    solve()
