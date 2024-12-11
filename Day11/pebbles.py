from argparse import ArgumentParser

def main(data):
    numbers = [int(no) for no in data[0].split()]

    for _ in range(25):
        next_numbers = []
        for number in numbers:
            if number == 0:
                next_numbers.append(1)
            elif not (len(str(number)) % 2):
                str_no = str(number)
                next_numbers.append(int(str_no[:len(str_no)//2]))
                next_numbers.append(int(str_no[len(str_no)//2:]))
            else:
                next_numbers.append(number * 2024)
        numbers = next_numbers

    print(len(numbers))

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
