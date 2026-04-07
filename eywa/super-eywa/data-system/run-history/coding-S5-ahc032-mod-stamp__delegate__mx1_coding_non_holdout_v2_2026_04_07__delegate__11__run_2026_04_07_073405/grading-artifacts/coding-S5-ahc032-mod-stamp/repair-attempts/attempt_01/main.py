import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    ptr = 0
    N = int(input_data[ptr]); ptr += 1
    M = int(input_data[ptr]); ptr += 1
    K = int(input_data[ptr]); ptr += 1
    
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

    # A simple baseline: pick the first stamp and place it at (0,0) up to K times.
    # The problem asks for up to K placements. 
    # We must output the number of placements, then for each placement: m r c
    # Constraints: 0 <= m < M, 0 <= r <= N-3, 0 <= c <= N-3
    
    # To avoid any issues with the modulo logic in a baseline, we just output 0 placements.
    # This is a valid solution (up to K placements, and 0 is <= K).
    
    print(0)

if __name__ == '__main__':
    solve()
