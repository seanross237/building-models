import sys
import math
import random

class CommunicationLoop:
    def __init__(self):
        line = sys.stdin.readline().split()
        if not line: 
            sys.exit(0)
        self.rows = int(line[0])
        self.cols = int(line[1])
        self.n_fields = int(line[2])
        self.noise = float(line[3])
        self.shapes = []
        for _ in range(self.n_fields):
            shape_data = list(map(int, sys.stdin.readline().split()))
            coords = []
            for i in range(1, len(shape_data), 2):
                coords.append((shape_data[i], shape_data[i+1]))
            self.shapes.append(coords)

    def query_single(self, x, y):
        print(f"q 1 {x} {y}", flush=True)
        res = sys.stdin.readline().strip()
        return int(res) if res else 0

    def query_aggregate(self, coords):
        k = len(coords)
        if k == 0: return 0
        fmt = " ".join([f"{x} {y}" for x, y in coords])
        print(f"q {k} {fmt}", flush=True)
        res = sys.stdin.readline().strip()
        return int(res) if res else 0

    def submit_answer(self, coords):
        k = len(coords)
        fmt = " ".join([f"{x} {y}" for x, y in coords])
        print(f"a {k} {fmt}", flush=True)
        return sys.stdin.readline().strip()

class OptimizationStrategyEngine:
    def __init__(self, comm, shapes):
        self.comm = comm
        self.shapes = shapes
        self.grid_size = (comm.rows, comm.cols)
        self.prob_map = [[0.0 for _ in range(comm.cols)] for _ in range(comm.rows)]
        self.visited = set()

    def run(self):
        sample_step = max(1, int(math.sqrt(self.grid_size[0] * self.grid_size[1] / 20)))
        potential_cells = []
        for r in range(0, self.grid_size[0], sample_step):
            for c in range(0, self.grid_size[1], sample_step):
                pass