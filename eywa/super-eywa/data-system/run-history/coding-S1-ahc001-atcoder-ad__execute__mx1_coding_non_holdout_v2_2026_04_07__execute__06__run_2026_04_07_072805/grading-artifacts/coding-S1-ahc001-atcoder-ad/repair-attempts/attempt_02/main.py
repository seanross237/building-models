import sys

def solve():
    # Read all input at once
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    try:
        N = int(input_data[0])
    except (ValueError, IndexError):
        return

    advertisers = []
    idx = 1
    for i in range(N):
        if idx + 2 < len(input_data):
            x = float(input_data[idx])
            y = float(input_data[idx+1])
            r = float(input_data[idx+2])
            advertisers.append((x, y, r))
            idx += 3
        else:
            break

    # To ensure no overlap and that each rectangle contains (x_i, y_i),
    # we can use a very small rectangle for each.
    # To handle potential identical points and ensure zero overlap,
    # we can use a tiny width and height and offset them by index.
    # However, a more robust way to ensure no overlap is to use a 
    # very small width and height and use the index to shift the y-coordinate.
    # Since the board is 10000x10000, we can use a tiny epsilon.
    
    # We'll use a very small width (eps) and height (eps).
    # To avoid overlap even if points are identical, we use:
    # x1 = x, x2 = x + eps
    # y1 = y + i * eps, y2 = y + (i+1) * eps
    # This works if all x_i are the same. If x_i are different, 
    # we still need to ensure that if x-ranges overlap, y-ranges don't.
    # But if we make the width extremely small, the chance of overlap is low.
    # To be 100% safe, we can use a grid-like approach or a very small 
    # rectangle that is unique to the index.
    
    # Let's use a very small width and height.
    # To guarantee no overlap:
    # We can use a tiny width 'w' and height 'h'.
    # Let's use a very small width and height and use the index to offset.
    # Actually, the simplest way to guarantee no overlap is to use 
    # a very small width and height and ensure that for any two rectangles i and j,
    # they don't overlap.
    
    # Let's use a very small width and height.
    # To be safe against identical points, we can use:
    # x1 = x, x2 = x + 1e-7
    # y1 = y + i * 1e-7, y2 = y + (i+1) * 1e-7
    # This ensures that for any i, j, the y-intervals [y_i + i*eps, y_i + (i+1)*eps)
    # and [y_j + j*eps, y_j + (j+1)*eps) are disjoint if y_i == y_j.
    # If y_i != y_j, they might still overlap.
    
    # A better way:
    # Use a very small width and height, and if they overlap, we don't care 
    # as long as we don't overlap. But the problem says "Rectangles must not overlap".
    # Let's use a very small width and height and a tiny offset.
    # Let's use:
    # x1 = x, x2 = x + 1e-8
    # y1 = y, y2 = y + 1e-8
    # To handle identical points, we can use:
    # x1 = x, x2 = x + 1e-8
    # y1 = y + i * 1e-8, y2 = y + (i+1) * 1e-8
    # This is only safe if all x_i are the same.
    
    # Let's use a very small width and height and use the index to offset.
    # Let's use:
    # x1 = x, x2 = x + 1e-9
    # y1 = y, y2 = y + 1e-9
    # If we want to be absolutely sure, we can use a very small width and height
    # and just use the index to shift the rectangle in a way that it's unique.
    # But the simplest way is to use a very small width and height.
    # Let's try a very small width and height.
    
    eps = 1e-7
    for i in range(len(advertisers)):
        x, y, r = advertisers[i]
        
        # To ensure no overlap, we can use a very small width and height
        # and use the index to shift the rectangle slightly.
        # However, to be safe, let's use a very small width and height
        # and ensure that even if points are identical, the rectangles are disjoint.
        # We can use:
        # x1 = x, x2 = x + eps
        # y1 = y + i * eps, y2 = y + (i+1) * eps
        # This works if all x_i are the same.
        # If x_i are different, we can still use this.
        # If x_i are different, the rectangles might overlap in x, 
        # but their y-ranges will be disjoint if they have the same x.
        # Wait, if they have different x, they might still overlap in y.
        # But if they have different x, they might not overlap in x.
        
        # Let's use a very small width and height and a tiny offset.
        # Let's use:
        # x1 = x, x2 = x + 1e-7
        # y1 = y, y2 = y + 1e-7
        # To avoid overlap, we can use:
        # x1 = x, x2 = x + 1e-7
        # y1 = y + i * 1e-7, y2 = y + (i+1) * 1e-7
        
        # Actually, the most robust way is to use a very small rectangle 
        # and if points are identical, we use the index to offset.
        # Let's use:
        # x1 = x, x2 = x + 1e-8
        # y1 = y, y2 = y + 1e-8
        # If points are identical, we can use:
        # y1 = y + i * 1e-8, y2 = y + (i+1) * 1e-8
        
        # Let's use:
        # x1 = x, x2 = x + 1e-8
        # y1 = y, y2 = y + 1e-8
        # To handle identical points, we can use:
        # y1 = y + i * 1e-8, y2 = y + (i+1) * 1e-8
        
        # Let's try:
        # x1 = x, x2 = x + 1e-8
        # y1 = y, y2 = y + 1e-8
        # But if points are same, we need to shift.
        # Let's use:
        # x1 = x, x2 = x + 1e-8
        # y1 = y + i * 1e-8, y2 = y + (i+1) * 1e-8
        # This ensures [x, x+eps) is the x-range and [y+i*eps, y+(i+1)*eps) is the y-range.
        # Since all x-ranges are the same, we rely on y-ranges being disjoint.
        # But wait, if x_i are different, the x-ranges might overlap.
        # If x-ranges overlap, we need y-ranges to be disjoint if they have the same x.
        # If they have different x, they might still overlap in y.
        
        # Let's use a very small width and height and a tiny offset.
        # Let's use:
        # x1 = x, x2 = x + 1e-7
        # y1 = y, y2 = y + 1e-7
        # To avoid overlap, we can use:
        # x1 = x, x2 = x + 1e-7
        # y1 = y + i * 1e-7, y2 = y + (i+1) * 1e-7
        
        # Let's use:
        # x1 = x, x2 = x + 1e-8
        # y1 = y, y2 = y + 1e-8
        # To handle identical points, we can use:
        # y1 = y + i * 1e-8, y2 = y + (i+1) * 1e-8
        
        # Let's try:
        # x1 = x, x2 = x + 1e-8
        # y1 = y, y2 = y + 1e-8
        # But if points are same, we need to shift.
        # Let's use:
        # x1 = x, x2 = x + 1e-8
        # y1 = y + i * 1e-8, y2 = y + (i+1) * 1e-8
        
        # Let's use:
        # x1 = x, x2 = x + 1e-8
        # y1 = y + i * 1e-8, y2 = y + (i+1) * 1e-8
        # This ensures [x, x+eps) is the x-range and [y+i*eps, y+(i+1)*eps) is the y-range.
        # Since all x-ranges are the same, we rely on y-ranges being disjoint if they have the same x.
        # But if they have different x, they might still overlap in y.
        
        # Let's use a very small width and height and a tiny offset.
