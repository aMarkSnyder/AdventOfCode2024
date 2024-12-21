from argparse import ArgumentParser

def valid_design(design, options, curr):
    if design == curr:
        return True
    if len(design) < len(curr):
        return False
    candidates = []
    for option in options:
        test = curr + option
        if test == design[:len(test)]:
            candidates.append(test)
    return any(valid_design(design, options, candidate) for candidate in candidates)

def main(data):
    options = data[0].split(', ')
    designs = data[2:]

    total_valid = 0
    for design in designs:
        if valid_design(design, options, ''):
            total_valid += 1
    print(total_valid)

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
