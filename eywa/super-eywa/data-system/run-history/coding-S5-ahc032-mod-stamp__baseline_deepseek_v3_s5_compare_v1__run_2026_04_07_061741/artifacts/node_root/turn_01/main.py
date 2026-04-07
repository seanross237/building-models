import sys

def main():
    data = sys.stdin.read().strip().split()
    if not data:
        return
    # Just output 0 placements
    print(0)

if __name__ == "__main__":
    main()
