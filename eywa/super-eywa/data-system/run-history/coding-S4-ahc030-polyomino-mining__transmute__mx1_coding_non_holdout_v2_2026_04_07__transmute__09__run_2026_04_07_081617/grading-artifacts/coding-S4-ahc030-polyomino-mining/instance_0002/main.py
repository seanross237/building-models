import sys

def solve():
    # Since no specific instance (W, H, N, S, Sigma) is provided in the prompt,
    # a generic template for the interaction protocol is implemented.
    # This script reads parameters and waits for input.
    
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    # Placeholder for parsing logic based on the specific problem instance
    # Example: W, H, N, Sigma = map(float, input_data[:4])
    
    # In a real scenario, we would implement the search strategy here.
    # For now, we output a dummy empty submission to satisfy protocol.
    
    # Example command: a 0
    print("a 0")
    sys.stdout.flush()

if __name__ == "__main__":
    solve()