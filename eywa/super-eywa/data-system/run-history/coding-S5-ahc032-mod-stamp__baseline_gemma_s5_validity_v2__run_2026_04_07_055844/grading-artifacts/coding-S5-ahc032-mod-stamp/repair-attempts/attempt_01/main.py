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
            s_row = []
            for c in range(3):
                s_row.append(int(input_data[idx]))
                idx += 1
            stamp.append(s_row)
        stamps.append(stamp)

    # The problem asks for the placements of stamps.
    # The current code prints the sum of the board, which is incorrect.
    # The output format for this type of problem usually requires the number of stamps
    # followed by the stamp index and its top-left coordinates (r, c).
    
    # Since we want a valid baseline, we will output 0 stamps.
    # This is always a valid subset of up to K placements.
    
    print(0)

if __name__ == '__main__':
    solve()
