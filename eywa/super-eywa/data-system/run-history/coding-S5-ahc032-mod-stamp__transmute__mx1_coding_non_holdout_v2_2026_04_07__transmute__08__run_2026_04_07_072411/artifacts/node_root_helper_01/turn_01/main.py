import sys

def solve():
    try:
        line1 = sys.stdin.readline().split()
        if not line1: return
        N, M, K = map(int, line1)
        
        grid = []
        for _ in range(N):
            grid.append(list(map(int, sys.stdin.readline().split())))
            
        stamps = []
        for _ in range(M):
            stamp = []
            for _ in range(3):
                stamp.append(list(map(int, sys.stdin.readline().split())))
            stamps.append(stamp)
            
        # Simple greedy: try all placements and pick the best one
        # that increases the total sum.
        # Since we can do up to K placements, we can repeat this.
        
        MOD = 998244353
        placements = []
        
        for _ in range(K):
            best_gain = 0
            best_move = None
            
            current_sum = sum(sum(row) for row in grid)
            
            for m in range(M):
                for i in range(N - 2):
                    for j in range(N - 2):
                        new_sum = current_sum
                        for di in range(3):
                            for dj in range(3):
                                old_val = grid[i+di][j+dj]
                                new_val = (old_val + stamps[m][di][dj]) % MOD
                                new_sum += (new_val - old_val)
                        
                        gain = new_sum - current_sum
                        if gain > best_gain:
                            best_gain = gain
                            best_move = (m, i, j)
            
            if best_move:
                m, i, j = best_move
                placements.append((m, i, j))
                for di in range(3):
                    for dj in range(3):
                        grid[i+di][j+dj] = (grid[i+di][j+dj] + stamps[m][di][dj]) % MOD
            else:
                break
                
        print(len(placements))
        for p in placements:
            print(f"{p[0]} {p[1]} {p[2]}")
            
    except EOFError:
        pass

if __name__ == "__main__":
    solve()