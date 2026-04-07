import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    N = int(input_data[0])
    targets = []
    for i in range(N):
        a = int(input_data[1 + 2*i])
        b = int(input_data[2 + 2*i])
        targets.append((a, b))
    
    targets.sort()
    
    existing_beverages = [(0, 0)]
    operations = []
    
    for tx, ty in targets:
        best_source_idx = -1
        min_dist = float('inf')
        
        for i, (fx, fy) in enumerate(existing_beverages):
            if fx <= tx and fy <= ty:
                dist = (tx - fx) + (ty - fy)
                if dist < min_dist:
                    min_dist = dist
                    best_source_idx = i
        
        if best_source_idx != -1:
            fx, fy = existing_beverages[best_source_idx]
            operations.append((fx, fy, tx, ty))
            existing_beverages.append((tx, ty))
