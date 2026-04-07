import sys

def solve():
    # Read initial input
    line = sys.stdin.readline()
    if not line:
        return
    parts = list(map(int, line.split()))
    if len(parts) < 4:
        return
    
    H, W, N_FIELDS, NOISE = parts[0:4]
    
    # The problem states "The rest of the input contains polyomino shapes."
    # We must consume these lines to reach the interaction phase.
    # Since the number of shapes isn't explicitly given in the first line,
    # we need to be careful. However, in AtCoder interactive problems, 
    # the shapes are usually provided as a fixed block.
    # Let's assume the shapes are provided until the end of the initial input block.
    # A common pattern is that the number of shapes is N_FIELDS or similar, 
    # but the prompt says "The rest of the input contains polyomino shapes".
    # We will read the remaining lines of the initial input.
    
    # In many competitive programming environments, we can read the rest of the 
    # lines provided in the initial input block.
    # However, since we don't know how many lines there are, we'll try to read 
    # until we hit an empty line or EOF, but the interaction starts immediately.
    # Actually, the most robust way is to read the shapes if they are provided.
    # Let's assume the shapes are provided line by line.
    
    # For a baseline, we don't strictly need the shapes to perform a brute-force scan.
    # We just need to ensure we don't try to read from stdin when the tester 
    # expects a query.
    
    # Let's skip the shapes by reading the rest of the lines that are NOT part of the interaction.
    # But how do we know when the shapes end? 
    # Usually, the number of shapes is given or the shapes are part of the first line.
    # Given the error in the previous code was likely a crash during reading,
    # let's assume the shapes are provided and we should consume them.
    # If the shapes are not provided, the loop below will just start.
    
    # Since we don't know the exact format of the shapes, and we want a robust 
    # baseline, we will attempt to read the shapes if they exist.
    # However, if we read too much, we might consume the response to our first query.
    # A safer way: the problem says "The rest of the input contains polyomino shapes."
    # This implies they are part of the initial input.
    
    # Let's try to read the shapes. We'll assume each shape is on its own line.
    # We'll stop reading if we encounter a line that looks like a response (a float).
    # But that's risky. Let's assume the shapes are provided and we can read them.
    # If the shapes are not provided, we'll just proceed.
    
    # Actually, the simplest way to handle "The rest of the input" is to read 
    # all lines and then decide. But we can't read all lines because 
    # interaction is interleaved.
    # Let's assume the shapes are provided in a way that we can read them 
    # before we start querying.
    
    # Let's try to read the shapes. We'll assume the number of shapes is N_FIELDS.
    # If that's not true, we'll just try to read N_FIELDS lines.
    for _ in range(N_FIELDS):
        sys.stdin.readline()

    oil_cells = []

    # Strategy: Scan the grid using single-cell queries 'q 1 x y'
    # We use a simple scan.
    for y in range(1, H + 1):
        for x in range(1, W + 1):
            # Query single cell
            print(f"q 1 {x} {y}", flush=True)
            
            # Read response
            resp_line = sys.stdin.readline()
            if not resp_line:
                break
            
            try:
                # The response is a float representing the presence/noise
                resp_val = float(resp_line.strip())
                # Thresholding: if the value is significantly above 0, it's likely oil.
                # Given NOISE is provided, 0.5 is a safe baseline.
                if resp_val > 0.5:
                    oil_cells.append((x, y))
            except ValueError:
                # If we get something that isn't a float, it might be an error or end of input
                break

    # Submit the final set of oil cells
    # Format: 'a k x1 y1 x2 y2 ... xk yk'
    if oil_cells:
        cmd = [f"a {len(oil_cells)}"]
        for ox, oy in oil_cells:
            cmd.append(str(ox))
            cmd.append(str(oy))
        print(" ".join(cmd), flush=True)
    else:
        print("a 0", flush=True)

if __name__ == "__main__":
    solve()
