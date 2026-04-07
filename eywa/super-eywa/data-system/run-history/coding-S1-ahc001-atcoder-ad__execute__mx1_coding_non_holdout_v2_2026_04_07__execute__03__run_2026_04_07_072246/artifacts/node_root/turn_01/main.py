import sys
import math

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    N = int(input_data[0])
    advertisers = []
    idx = 1
    for i in range(N):
        x = float(input_data[idx])
        y = float(input_data[idx+1])
        r = float(input_data[idx+2])
        advertisers.append({'id': i, 'x': x, 'y': y, 'r': r})
        idx += 3

    sorted_adv = sorted(advertisers, key=lambda a: a['r'], reverse=True)
    
    results = [None] * N
    eps = 1e-7
    
    for adv in advertisers:
        x, y = adv['x'], adv['y']
        x1 = max(0.0, x - eps)
        y1 = max(0.0, y - eps)
        x2 = min(10000.0, x + eps)
        y2 = min(10000.0, y + eps)
        
        if x1 == x2: x2 += eps
        if y1 == y2: y2 += eps
        
        if x2 > 10000.0: 
            x2 = 10000.0
            x1 = max(0.0, x2 - eps)
