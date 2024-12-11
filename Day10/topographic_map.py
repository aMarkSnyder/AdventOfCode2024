from argparse import ArgumentParser
import numpy as np

def valid(grid, point):
    return 0 <= point[0] < grid.shape[0] and 0 <= point[1] < grid.shape[1]

def find_summits(grid, start):
    if not valid(grid, start):
        return set()
    start_val = grid[start]
    if start_val == 9:
        return {start}
    else:
        summits = set()
        target = start_val + 1
        for step in ((0,1),(0,-1),(1,0),(-1,0)):
            point = (start[0]+step[0], start[1]+step[1])
            if valid(grid, point) and grid[point] == target:
                summits = summits.union(find_summits(grid, point))
        return summits
    
def find_paths(grid, start, path_so_far):
    if not valid(grid, start):
        return set()
    start_val = grid[start]
    if start_val == 9:
        return {path_so_far}
    else:
        paths = set()
        target = start_val + 1
        for step in ((0,1),(0,-1),(1,0),(-1,0)):
            point = (start[0]+step[0], start[1]+step[1])
            if valid(grid, point) and grid[point] == target:
                paths = paths.union(find_paths(grid, point, path_so_far+(point,)))
        return paths

def main(data):
    grid = np.array([[int(val) for val in row] for row in data])

    total_score = 0
    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if grid[row,col] == 0:
                total_score += len(find_summits(grid, (row,col)))
    print(total_score)

    total_rating = 0
    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if grid[row,col] == 0:
                total_rating += len(find_paths(grid, (row,col), ((row,col),)))
    print(total_rating)

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
