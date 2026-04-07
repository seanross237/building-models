#!/usr/bin/env python3
import sys

def main():
    # Read input (not used) and output zero placements as a valid baseline
    try:
        sys.stdin.read()
    except Exception:
        pass
    print(0)

if __name__ == '__main__':
    main()
