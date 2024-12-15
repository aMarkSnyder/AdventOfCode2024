from argparse import ArgumentParser
import numpy as np

DIRS = {
    '^': (-1, 0),
    '>': (0, 1),
    'v': (1, 0),
    '<': (0, -1),
}

def main(data):
    empty = data.index('')
    warehouse = np.array([[char for char in row] for row in data[:empty]])
    instructions = ''.join(data[empty+1:])
    
    start = (-1, -1)
    for row in range(warehouse.shape[0]):
        for col in range(warehouse.shape[1]):
            if warehouse[row,col] == '@':
                start = (row, col)
                break

    robot = start
    for instr in instructions:
        step = DIRS[instr]
        curr = (robot[0]+step[0], robot[1]+step[1])
        while warehouse[curr] == 'O':
            curr = (curr[0]+step[0], curr[1]+step[1])
        if warehouse[curr] == '.':
            while curr != robot:
                warehouse[curr] = warehouse[(curr[0]-step[0], curr[1]-step[1])]
                curr = (curr[0]-step[0], curr[1]-step[1])
            warehouse[robot] = '.'
            robot = (robot[0]+step[0], robot[1]+step[1])

    total = 0
    for row in range(warehouse.shape[0]):
        for col in range(warehouse.shape[1]):
            if warehouse[row,col] == 'O':
                total += 100*row + col
    print(total)


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
