import sys

def solve():
    try:
        line = sys.stdin.readline()
        if not line:
            return
        board = []
        for _ in range(9):
            board.append(list(map(int, sys.stdin.readline().split())))
        
        m_count = int(sys.stdin.readline())
        stamps = []
        for _ in range(m_count):
            stamps.append(list(map(int, sys.stdin.readline().split())))
        
        k_limit = int(sys.stdin.readline())
    except EOFError:
        return
    except ValueError:
        return

    # A simple baseline: print 0 placements
    print(0)

if __name__ == '__main__':
    solve()