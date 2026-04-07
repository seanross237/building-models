def main():
    # Read input parameters
    N, M, K = map(int, input().split())
    
    # Read initial board
    board = [list(map(int, input().split())) for _ in range(N)]
    
    # Read stamps (not used in this minimal solution)
    for _ in range(M):
        for _ in range(3):
            input()
    
    # Output zero placements
    print(0)

if __name__ == '__main__':
    main()