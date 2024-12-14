from argparse import ArgumentParser
import re
from dataclasses import dataclass
from math import prod
import numpy as np

@dataclass
class Robot:
    x: int
    y: int
    vx: int
    vy: int

    def advance(self, steps, x_lim=None, y_lim=None):
        self.x += steps*self.vx
        if x_lim:
            self.x %= x_lim
        self.y += steps*self.vy
        if y_lim:
            self.y %= y_lim

def all_ints(s):
    return [int(i) for i in re.findall(r'-?\b\d+\b', s)]

def check_robot_uniqueness(robots, min_unique=0.8):
    locs = set()
    for robot in robots:
        if (robot.x, robot.y) in locs:
            break
        locs.add((robot.x,robot.y))
    return len(locs)/len(robots) >= min_unique

def gridify_robots(robots, x_lim, y_lim):
    grid = np.zeros((y_lim, x_lim))
    for robot in robots:
        grid[(robot.y,robot.x)] += 1
    return grid

def main(data):
    robots = []
    for line in data:
        robots.append(Robot(*all_ints(line)))

    x_lim, y_lim = 101, 103
    for robot in robots:
        robot.advance(100, x_lim, y_lim)

    quadrant_totals = [0] * 4
    for robot in robots:
        if robot.y < y_lim//2:
            if robot.x < x_lim//2:
                quadrant_totals[0] += 1
            elif robot.x > x_lim//2:
                quadrant_totals[1] += 1
        elif robot.y > y_lim//2:
            if robot.x < x_lim//2:
                quadrant_totals[2] += 1
            elif robot.x > x_lim//2:
                quadrant_totals[3] += 1
    print(prod(quadrant_totals))

    robots = []
    for line in data:
        robots.append(Robot(*all_ints(line)))

    for sec in range(100000):
        if check_robot_uniqueness(robots, min_unique=.9):
            print(f'Unique robots after {sec} seconds!')
            np.savetxt(f'robots_{sec}.txt', gridify_robots(robots, x_lim, y_lim), fmt="%1d", delimiter='')
        for robot in robots:
            robot.advance(1, x_lim, y_lim)


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
