from itertools import cycle
import numpy as np

FORWARD_CYCLE = cycle('MAS')

def check_for_xmas_in_direction(grid, row, col, delta):
    valid = True
    for _ in range(3):
        row += delta[0]
        col += delta[1]
        expected_char = next(FORWARD_CYCLE)
        if grid[row,col] != expected_char:
            valid = False
    return valid

def check_for_xmas_at_position(grid, row, col):
    xmas_starting_here = 0
    if grid[row,col] != 'X':
        return xmas_starting_here

    max_row, max_col = grid.shape

    # verticals
    if row <= max_row - 4:
        xmas_starting_here += check_for_xmas_in_direction(grid, row, col, (1, 0))
    if row >= 3:
        xmas_starting_here += check_for_xmas_in_direction(grid, row, col, (-1, 0))
    
    # horizontals
    if col <= max_col - 4:
        xmas_starting_here += check_for_xmas_in_direction(grid, row, col, (0, 1))
    if col >= 3:
        xmas_starting_here += check_for_xmas_in_direction(grid, row, col, (0, -1))

    # diagonals
    if row <= max_row - 4:
        if col <= max_col - 4:
            xmas_starting_here += check_for_xmas_in_direction(grid, row, col, (1, 1))
        if col >= 3:
            xmas_starting_here += check_for_xmas_in_direction(grid, row, col, (1, -1))

    if row >= 3:
        if col <= max_col - 4:
            xmas_starting_here += check_for_xmas_in_direction(grid, row, col, (-1, 1))
        if col >= 3:
            xmas_starting_here += check_for_xmas_in_direction(grid, row, col, (-1, -1))

    return xmas_starting_here

def check_for_x_mas_at_position(grid, row, col):
    if grid[row, col] != 'A':
        return 0

    max_row, max_col = grid.shape
    if (not 1 <= row < max_row-1) or (not 1 <= col < max_col-1):
        return 0

    ul = grid[row-1, col-1]
    ur = grid[row-1, col+1]
    ll = grid[row+1, col-1]
    lr = grid[row+1, col+1]

    if any(corner not in 'MS' for corner in (ul, ur, ll, lr)):
        return 0

    if not (ul != lr and ur != ll):
        return 0
    
    return 1

lines = []
with open('input.txt','r') as input:
    for line in input:
        lines.append(line.strip())

# Star 1
char_array = np.array([[char for char in line] for line in lines])

total = 0
for row in range(char_array.shape[0]):
    for col in range(char_array.shape[1]):
        total += check_for_xmas_at_position(char_array, row, col)
print(total)

# Star 2
total = 0
for row in range(char_array.shape[0]):
    for col in range(char_array.shape[1]):
        total += check_for_x_mas_at_position(char_array, row, col)
print(total)
