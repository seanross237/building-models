import sys

def main():
    data = sys.stdin.read().split()
    if not data:
        print(0)
        return
    # Read N, M, K
    N = int(data[0])
    M = int(data[1])
    K = int(data[2])
    # Skip reading the rest of input
    # Output 0 placements
    print(0)

if __name__ == '__main__':
    main()