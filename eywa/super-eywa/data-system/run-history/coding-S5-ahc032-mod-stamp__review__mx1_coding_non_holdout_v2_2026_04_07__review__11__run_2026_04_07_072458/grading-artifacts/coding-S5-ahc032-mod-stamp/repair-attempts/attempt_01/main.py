import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    ptr = 0
    N = int(input_data[ptr]); ptr += 1
    M = int(input_data[ptr]); ptr += 1
    K = int(input_data[ptr]); ptr += 1
    
    board_size = 9
    board = []
    for i in range(board_size):
        row = []
        for j in range(board_size):
            row.append(int(input_data[ptr]))
            ptr += 1
        board.append(row)
        
    MOD = 998244353
    
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

    # A simple baseline: output 0 placements.
    # The problem asks for up to K placements. 
    # The output format for AHC usually requires the number of placements followed by the placements.
    # Based on the problem description, we output the number of stamps used, then for each stamp: m r c.
    
    print(0)

if __name__ == '__main__':
    solve()
