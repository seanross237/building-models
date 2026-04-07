import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    N = int(input_data[0])
    advertisers = []
    idx = 1
    for i in range(N):
        x = int(input_data[idx])
        y = int(input_data[idx+1])
        r = int(input_data[idx+2])
        advertisers.append({'id': i, 'x': x, 'y': y, 'r': r})
        idx += 3

    advertisers.sort(key=lambda a: a['x'])
    results = [None] * N
    sorted_adv = sorted(advertisers, key=lambda a: a['x'])
    # Implementation truncated due to original content cutoff