import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    try:
        N = int(input_data[0])
    except ValueError:
        return

    idx = 1
    results = []
    for _ in range(N):
        if idx + 2 >= len(input_data):
            break
        # The scorer expects integers for input, but the contestant
        # was reading floats. We use int() to match the scorer's expectation
        # of i64 based on the error message.
        try:
            x = int(float(input_data[idx]))
            y = int(float(input_data[idx+1]))
            r = int(float(input_data[idx+2]))
        except ValueError:
            # Fallback if input is actually float-formatted strings
            x = int(float(input_data[idx]))
            y = int(float(input_data[idx+1]))
            r = int(float(input_data[idx+2]))
            
        idx += 3
        
        # To avoid overlapping and ensure valid rectangles,
        # we output a tiny rectangle around the point.
        # Using integer coordinates to avoid precision issues if the scorer expects them,
        # but the problem asks for rectangles. Let's use x, x+1, y, y+1 if possible,
        # but the simplest valid baseline is a tiny area.
        # Given the error 'failed to parse 4335.0 to i64', the input is likely
        # provided as floats but the scorer reads them as i64. 
        # We will output integer coordinates to be safe.
        results.append(f"{x} {x+1} {y} {y+1}")
    
    if results:
        sys.stdout.write("\n".join(results) + "\n")

if __name__ == "__main__":
    solve()
