import numpy as np
    
def get_step_and_n_dir(direction):
    match direction:
        case '^':
            step = (-1,0)
            n_dir = '>'
        case '>':
            step = (0,1)
            n_dir = 'v'
        case 'v':
            step = (1,0)
            n_dir = '<'
        case '<':
            step = (0,-1)
            n_dir = '^'
    return step, n_dir

def solve_maze(grid, start, direction):
    visited = {start}
    history = {(start, direction)}
    max_row, max_col = grid.shape
    step, n_dir = get_step_and_n_dir(direction)
    pos = start
    while True:
        n_pos = (pos[0] + step[0], pos[1] + step[1])

        if not (0 <= n_pos[0] < max_row and 0 <= n_pos[1] < max_col):
            return visited
        
        if (n_pos, direction) in history:
            return set()

        if grid[n_pos] == '#':
            direction = n_dir
            step, n_dir = get_step_and_n_dir(direction)

        else:
            pos = n_pos
            visited.add(pos)
            history.add((pos, direction))

lines = []
with open('input.txt','r') as input:
    for line in input:
        lines.append(line.strip())

# Star 1
char_array = np.array([[char for char in line] for line in lines])

start = (-1,-1)
max_row, max_col = char_array.shape
for row in range(max_row):
    for col in range(max_col):
        if char_array[row,col] not in '.#':
            start = (row,col)
            direction = char_array[row,col]
            break
    if start != (-1, -1):
        break

char_array[start] = '.'

obstacles = set()
visited = solve_maze(char_array, start, direction)
print(len(visited))

obstacles = set()
for pos in visited:
    if pos != start:
        char_array[pos] = '#'
        if not solve_maze(char_array, start, direction):
            obstacles.add(pos)
        char_array[pos] = '.'
print(len(obstacles))
