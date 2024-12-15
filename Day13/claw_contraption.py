from argparse import ArgumentParser
from dataclasses import dataclass
import numpy as np
import re

def all_ints(s):
    return [int(i) for i in re.findall(r'-?\b\d+\b', s)]

@dataclass
class ClawMachine:
    ax: int
    ay: int
    bx: int
    by: int
    px: int
    py: int

    def solve(self):
        # ax * a + bx * b == px -> a == (px - bx*b) / ax
        # ay * a + by * b == py -> ay/ax * (px - bx*b) + by*b == py -> ay/ax * px - ay/ax * bx * b + by * b == py
        # -> b * (by - ay/ax * bx) == py - ay/ax * px -> b == (py - ay/ax * px) / (by - ay/ax * bx)

        coeffs = np.array([[self.ax, self.bx], [self.ay, self.by]])
        ords = np.array([self.px, self.py])

        return np.linalg.solve(coeffs, ords)
    
    def valid_soln(self, a, b, limit):
        return (0 <= a <= limit) and (0 <= b <= limit) and (self.ax*a+self.bx*b==self.px) and (self.ay*a+self.by*b==self.py)
    
    def tokens(self, a_cost=3, b_cost=1, limit=100):
        a, b = self.solve()
        a, b = np.round(a), np.round(b)
        if self.valid_soln(a, b, limit):
            return a_cost*a + b_cost*b
        return 0

def main(data):
    machines = []
    for start_idx in range(0, len(data), 4):
        ax, ay = all_ints(data[start_idx])
        bx, by = all_ints(data[start_idx+1])
        px, py = all_ints(data[start_idx+2])
        machines.append(ClawMachine(ax, ay, bx, by, px, py))

    print(sum(machine.tokens() for machine in machines))

    for machine in machines:
        machine.px += 10000000000000
        machine.py += 10000000000000

    print(sum(machine.tokens(limit=np.inf) for machine in machines))

def read_input(input_file):
    data = []
    with open(input_file, 'r') as input:
        for line in input:
            data.append(line.strip())
    return data

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('input_file', nargs='?', default='input.txt')
    args = parser.parse_args()
    data = read_input(args.input_file)
    main(data)
