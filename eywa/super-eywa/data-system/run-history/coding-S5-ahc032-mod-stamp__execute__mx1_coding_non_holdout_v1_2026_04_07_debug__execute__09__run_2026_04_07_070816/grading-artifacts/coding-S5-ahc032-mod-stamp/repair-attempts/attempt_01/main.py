import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    ptr = 0
    N = int(input_data[ptr])
    M = int(input_data[ptr+1])
    K = int(input_data[ptr+2])
    ptr += 3
    
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

    # Greedy approach:
    # Find the stamp and position that adds the most value to the current board sum.
    # Since we are working modulo 998244353, the "value" is tricky.
    # However, the problem asks to maximize the sum of final entries.
    # A simple greedy strategy: pick the stamp and position that increases the sum the most.
    # Note: The sum is calculated AFTER all additions are done modulo 998244353.
    # This makes local greedy difficult. 
    # But if we assume the values don't wrap around too often, or we just want a 
    # decent baseline, we can try to pick stamps with large positive values.
    
    MOD = 998244353
    
    current_board = [row[:] for row in board]
    placements = []
    
    # To avoid complex modulo logic in a simple greedy, 
    # let's just pick the best stamp/position based on the raw sum of the stamp.
    # We'll try to place stamps that have the largest sum of elements.
    
    stamp_sums = []
    for m in range(M):
        s = 0
        for i in range(3):
            for j in range(3):
                s += stamps[m][i][j]
        stamp_sums.append((s, m))
    
    stamp_sums.sort(key=lambda x: x[0], reverse=True)
    
    # Try to place the best stamp at every possible position until K is reached.
    # To keep it simple and valid, we just place the best stamp at (0,0), (0,1)...
    # until we hit K or run out of space.
    
    count = 0
    for m_idx in range(M):
        m = stamp_sums[m_idx][1]
        for i in range(N - 2):
            for j in range(N - 2):
                if count < K:
                    placements.append((m, i, j))
                    count += 1
                else:
                    break
            if count >= K: break
        if count >= K: break

    print(len(placements))
    for p in placements:
        print(f"{p[0]} {p[1]} {p[2]}")

if __name__ == '__main__':
    solve()
