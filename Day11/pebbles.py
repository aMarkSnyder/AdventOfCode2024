from argparse import ArgumentParser
from functools import cache

@cache
def num_spawned(number, blinks):
    if not blinks:
        return 1
    else:
        if number == 0:
            return num_spawned(1, blinks-1)
        elif not (len(str(number)) % 2):
            str_no = str(number)
            return num_spawned(int(str_no[:len(str_no)//2]), blinks-1) + num_spawned(int(str_no[len(str_no)//2:]), blinks-1)
        else:
            return num_spawned(number*2024, blinks-1)

def main(data):
    numbers = [int(no) for no in data[0].split()]

    print(sum(num_spawned(number, 25) for number in numbers))
    print(sum(num_spawned(number, 75) for number in numbers))

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
