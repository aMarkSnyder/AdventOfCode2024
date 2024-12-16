from argparse import ArgumentParser
from dataclasses import dataclass
from heapq import *
import numpy as np
from collections import defaultdict

DIRS = [(0, 1), (1, 0), (0, -1), (-1, 0)] #ESWN

@dataclass(frozen=True, order=True)
class ReindeerState:
    cost: int
    loc: tuple
    dir: int

    def get_options(self, maze):
        options = []
        forward = (self.loc[0]+DIRS[self.dir][0], self.loc[1]+DIRS[self.dir][1])
        if maze[forward] == '.':
            options.append(ReindeerState(self.cost+1, forward, self.dir))

        left_step = DIRS[(self.dir-1) % len(DIRS)]
        left = (self.loc[0]+left_step[0], self.loc[1]+left_step[1])
        if maze[left] == '.':
            options.append(ReindeerState(self.cost+1001, left, (self.dir-1) % len(DIRS)))

        right_step = DIRS[(self.dir+1) % len(DIRS)]
        right = (self.loc[0]+right_step[0], self.loc[1]+right_step[1])
        if maze[right] == '.':
            options.append(ReindeerState(self.cost+1001, right, (self.dir+1) % len(DIRS)))

        return options
    
def count_visits(maze, start, goal, target_score, path_so_far, visits_by_optimal=defaultdict(int)):
    if start.cost > target_score:
        return
    if start.cost == target_score and start.loc == goal:
        for loc in path_so_far:
            visits_by_optimal[loc] += 1
        return
    
    options = start.get_options(maze)
    for option in options:
        count_visits(maze, option, goal, target_score, path_so_far + (option.loc,), visits_by_optimal)

def main(data):
    maze = {}
    distance = {}
    for row_idx, row in enumerate(data):
        for col_idx, val in enumerate(row):
            if val == 'S':
                start = ReindeerState(0, (row_idx, col_idx), 0)
                distance[(row_idx, col_idx)] = 0
                maze[(row_idx, col_idx)] = '.'
            elif val == 'E':
                goal = (row_idx, col_idx)
                distance[(row_idx, col_idx)] = np.inf
                maze[(row_idx, col_idx)] = '.'
            else:
                distance[(row_idx, col_idx)] = np.inf
                maze[(row_idx, col_idx)] = val

    queue = [start]
    while queue:
        curr = heappop(queue)
        if curr.cost > distance[goal]:
            break
        options = curr.get_options(maze)
        for option in options:
            if option.cost < distance[option.loc]:
                distance[option.loc] = option.cost
                heappush(queue, option)
    
    print(distance[goal])

    shortest_distance = distance[goal]
    visits_by_optimal = defaultdict(int)
    count_visits(maze, start, goal, shortest_distance, (start.loc,), visits_by_optimal)
    print(len(visits_by_optimal))

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
