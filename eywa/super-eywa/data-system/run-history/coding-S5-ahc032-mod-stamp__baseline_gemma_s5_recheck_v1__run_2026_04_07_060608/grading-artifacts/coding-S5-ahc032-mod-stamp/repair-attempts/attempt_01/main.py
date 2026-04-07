import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    idx = 0
    N = int(input_data[idx]); idx += 1
    M = int(input_data[idx]); idx += 1
    K = int(input_data[idx]); idx += 1
    
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
        for i in range(3):
            row = []
            for j in range(3):
                row.append(int(input_data[idx]))
                idx += 1
            stamp.append(row)
        stamps.append(stamp)

    # The problem asks for the placements of stamps, not the final sum.
    # The current code prints the sum, which is why the scorer says 'Out of range'.
    # A valid output should be the number of stamps used, followed by the stamp index, r, and c.
    
    placements = []
    # Greedy approach to find placements
    # Note: The problem asks to maximize sum modulo 998244353. 
    # Since modulo is large and values are likely positive, we treat it as maximizing the sum.
    
    current_board = [row[:] for row in board]
    
    for _ in range(K):
        best_gain = -1
        best_move = None
        
        for m in range(M):
            for r in range(N - 2):
                for c in range(N - 2):
                    gain = 0
                    for dr in range(3):
                        for dc in range(3):
                            gain += stamps[m][dr][dc]
                    
                    if gain > best_gain:
                        best_gain = gain
                        best_move = (m, r, c)
        
        if best_move:
            m, r, c = best_move
            placements.append((m, r, c))
            for dr in range(3):
                for dc in range(3):
                    current_board[r + dr][c + dc] = (current_board[r + dr][c + dc] + stamps[m][dr][dc]) % 998244353
        else:
            break

    # Output format: 
    # Number of placements
    # For each placement: m r c
    print(len(placements))
    for m, r, c in placements:
        print(f"{m} {r} {c}")

if __name__ == '__main__':
    solve()
