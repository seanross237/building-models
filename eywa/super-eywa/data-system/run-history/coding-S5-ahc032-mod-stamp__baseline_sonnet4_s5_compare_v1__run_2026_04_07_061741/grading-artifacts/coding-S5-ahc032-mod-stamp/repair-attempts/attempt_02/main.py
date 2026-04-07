def main():
    MOD = 998244353
    
    # Read input
    N, M, K = map(int, input().split())
    
    # Read initial board
    board = []
    for i in range(N):
        row = list(map(int, input().split()))
        board.append(row)
    
    # Read stamps
    stamps = []
    for m in range(M):
        stamp = []
        for i in range(3):
            row = list(map(int, input().split()))
            stamp.append(row)
        stamps.append(stamp)
    
    placements = []
    
    # Greedy approach: repeatedly find the best stamp placement
    for _ in range(K):
        best_score_increase = 0
        best_placement = None
        
        # Try each stamp at each valid position
        for m in range(M):
            for i in range(N - 2):  # top-left can be at most N-3
                for j in range(N - 2):
                    # Calculate score increase for this placement
                    score_increase = 0
                    for di in range(3):
                        for dj in range(3):
                            old_val = board[i + di][j + dj]
                            new_val = (old_val + stamps[m][di][dj]) % MOD
                            score_increase += new_val - old_val
                    
                    if score_increase > best_score_increase:
                        best_score_increase = score_increase
                        best_placement = (m, i, j)
        
        # If no beneficial placement found, stop
        if best_placement is None or best_score_increase <= 0:
            break
        
        # Apply the best placement
        m, i, j = best_placement
        placements.append((m, i, j))
        
        # Update board
        for di in range(3):
            for dj in range(3):
                board[i + di][j + dj] = (board[i + di][j + dj] + stamps[m][di][dj]) % MOD
    
    # Output
    print(len(placements))
    for m, i, j in placements:
        print(m, i, j)  # Keep 0-indexed

if __name__ == '__main__':
    main()
