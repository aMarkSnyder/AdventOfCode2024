from argparse import ArgumentParser
import numpy as np
from dataclasses import dataclass, field
np.set_printoptions(linewidth=180)

DIRS = {
    '^': (-1, 0),
    '>': (0, 1),
    'v': (1, 0),
    '<': (0, -1),
}

@dataclass
class Box:
    id: int
    locs: set = field(default_factory=set)

    def __hash__(self):
        return hash(self.id)

    def test_push(self, boxes, walls, instr):
        step = DIRS[instr]
        goals = {(loc[0]+step[0], loc[1]+step[1]) for loc in self.locs}
        affected_boxes = set()
        for goal in goals:
            if goal in walls:
                return -1
            for box in boxes:
                if goal in box.locs:
                    affected_boxes.add(box)
        return affected_boxes
    
    def push(self, instr):
        step = DIRS[instr]
        self.locs = {(loc[0]+step[0], loc[1]+step[1]) for loc in self.locs}

    def gps(self):
        return min(100*loc[0] + loc[1] for loc in self.locs)

@dataclass
class Robot(Box):
    id: int = -1
    locs: set = field(default_factory=set)

def complete_warehouse(warehouse, instructions):
    boxes = set()
    box_id = 0
    walls = set()
    for row in range(warehouse.shape[0]):
        for col in range(warehouse.shape[1]):
            match warehouse[row,col]:
                case '#':
                    walls.add((row,col))
                case 'O':
                    boxes.add(Box(box_id, {(row,col)}))
                    box_id += 1
                case '[':
                    boxes.add(Box(box_id, {(row,col),(row,col+1)}))
                    box_id += 1
                case '@':
                    robot = Robot(locs={(row,col)})

    for instr in instructions:
        affected_boxes = robot.test_push(boxes, walls, instr)
        if affected_boxes == -1:
            continue
        boxes_to_process = list(affected_boxes)
        blocked = False
        while boxes_to_process:
            curr = boxes_to_process.pop()
            affected = curr.test_push(boxes, walls, instr)
            if affected == -1:
                blocked = True
                break
            for box in affected:
                if box not in affected_boxes:
                    boxes_to_process.append(box)
                    affected_boxes.add(box)
        if not blocked:
            robot.push(instr)
            for box in affected_boxes:
                box.push(instr)

    return robot, boxes

def main(data):
    empty = data.index('')
    warehouse = np.array([[char for char in row] for row in data[:empty]])
    instructions = ''.join(data[empty+1:])

    _, boxes = complete_warehouse(warehouse, instructions)
    print(sum(box.gps() for box in boxes))

    big_data = []
    for row in data[:empty]:
        big_row = ''
        for char in row:
            match char:
                case '#':
                    big_row += '##'
                case 'O':
                    big_row += '[]'
                case '.':
                    big_row += '..'
                case '@':
                    big_row += '@.'
        big_data.append(big_row)
    big_warehouse = np.array([[char for char in row] for row in big_data])

    _, boxes = complete_warehouse(big_warehouse, instructions)
    print(sum(box.gps() for box in boxes))

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
