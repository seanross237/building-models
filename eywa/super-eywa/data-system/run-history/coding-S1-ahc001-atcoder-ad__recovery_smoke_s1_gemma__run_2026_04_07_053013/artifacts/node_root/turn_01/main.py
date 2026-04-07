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

    sorted_adv = sorted(advertisers, key=lambda a: a['r'], reverse=True)
    results = [None] * N
    occupied = []
    BOARD_SIZE = 10000

    def intersects(rect1, rect2):
        x1_a, y1_a, x2_a, y2_a = rect1
        x1_b, y1_b, x2_b, y2_b = rect2
        return not (x2_a <= x1_b or x2_b <= x1_a or y2_a <= y1_b or y2_b <= y1_a)

    for adv in sorted_adv:
        target_x, target_y, target_r = adv['x'], adv['y'], adv['r']
        best_rect = (target_x, target_y, target_x + 1, target_y + 1)
        best_area = 1
        curr_x1, curr_y1 = target_x, target_y
        curr_x2, curr_y2 = target_x + 1, target_y + 1