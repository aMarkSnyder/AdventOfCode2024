from argparse import ArgumentParser
from functools import cache

@cache
def valid_design(remaining, options):
    if remaining == '':
        return True
    candidates = []
    for option in options:
        if option == remaining[:len(option)]:
            candidates.append(remaining[len(option):])
    return sum(valid_design(candidate, options) for candidate in candidates)

def main(data):
    options = tuple(data[0].split(', '))
    designs = data[2:]

    total_valid = 0
    total_count = 0
    for design in designs:
        count = valid_design(design, options)
        if count:
            total_valid += 1
            total_count += count

    print(total_valid)
    print(total_count)

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
