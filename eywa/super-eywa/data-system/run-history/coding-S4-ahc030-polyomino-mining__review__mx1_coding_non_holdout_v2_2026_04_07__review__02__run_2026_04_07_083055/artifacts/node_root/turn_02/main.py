import sys

def solve():
    # Read initial input
    try:
        line = sys.stdin.readline()
        if not line:
            return
        parts = list(map(int, line.split()))
        if len(parts) < 4:
            return
        
        H, W, N_OIL, NOISE = parts[0], parts[1], parts[2], parts[3]
        
        # The next part of input is the polyomino shapes
        # Since the number of shapes isn't explicitly given in the first line, 
        # we assume the shapes are provided until the end of the input stream 
        # or we handle it based on the problem structure.
        # However, for a baseline, we focus on the grid search.
        
        # For this baseline, we will perform a grid scan using single-cell queries.
        # In a real competition, we would use the polyomino shapes to optimize the search.
        
        oil_cells = []
        
        # Simple scan strategy: query every cell to find oil.
        # Note: In a high-cost scenario, we would use 'q k' (multi-cell) queries 
        # to narrow down regions first.
        
        for r in range(H):
            for c in range(W):
                # Query single cell (q 1 x y)
                # Coordinates are usually 1-indexed in these problems, 
                # but we'll use 1-based indexing for the command.
                print(f"q 1 {r+1} {c+1}", flush=True)
                
                response = sys.stdin.readline().strip()
                if not response:
                    break
                
                # The response is typically 1 if oil is present, 0 otherwise
                # (or a noisy value depending on the noise parameter)
                if response == '1':
                    oil_cells.append((r+1, c+1))
            if not response:
                break

        # Submit the final set of oil cells
        # Format: a k x1 y1 x2 y2 ... xk yk
        if oil_cells:
            cmd = ["a", str(len(oil_cells))]
            for r, c in oil_cells:
                cmd.append(str(r))
                cmd.append(str(c))
            print(" ".join(cmd), flush=True)
        else:
            # Submit empty if no oil found
            print("a 0", flush=True)

    except EOFError:
        pass
    except Exception:
        pass

if __name__ == "__main__":
    solve()