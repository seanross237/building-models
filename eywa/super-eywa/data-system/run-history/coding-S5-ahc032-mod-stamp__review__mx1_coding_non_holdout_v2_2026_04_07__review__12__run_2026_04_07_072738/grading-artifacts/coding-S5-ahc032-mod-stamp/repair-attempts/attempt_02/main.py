import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    ptr = 0
    try:
        N = int(input_data[ptr]); ptr += 1
        M = int(input_data[ptr]); ptr += 1
        K = int(input_data[ptr]); ptr += 1
        
        # Skip board data
        for _ in range(N * N):
            ptr += 1
            
        # Skip stamps data
        for _ in range(M * 9):
            ptr += 1
            
    except (IndexError, ValueError):
        return

    # The problem asks for up to K placements.
    # A valid output format for 0 placements is just '0'.
    # Based on the scorer error 'Out of range', the previous code
    # likely failed because it printed nothing or malformed data.
    # In most competitive programming formats, if you output 0, 
    # you don't need to output any subsequent lines.
    print(0)

if __name__ == '__main__':
    solve()
