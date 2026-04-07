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
        stamp_sum = 0
        for r in range(3):
            row = []
            for c in range(3):
                val = int(input_data[ptr])
                ptr += 1
                row.append(val)
                stamp_sum += val
            stamp.append(row)
        stamps.append({'id': m, 'data': stamp, 'sum': stamp_sum})

    # Find the stamp with the maximum sum
    best_stamp = max(stamps, key=lambda x: x['sum'])
    
    placements = []
    # Valid top-left positions (i, j) such that 3x3 fits in NxN
    # Since N=9 and stamp is 3x3, i and j can range from 0 to 6
    for i in range(N - 2):
        for j in range(N - 2):
            if len(placements) < K:
                placements.append((best_stamp['id'], i, j))
            else:
                break
        if len(placements) >= K:
            break
            
    print(len(placements))
    for p in placements:
        print(f"{p[0]} {p[1]} {p[2]}")

if __name__ == "__main__":
    solve()