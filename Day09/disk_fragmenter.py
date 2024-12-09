from argparse import ArgumentParser
from dataclasses import dataclass

@dataclass
class DataRange():
    start: int
    end: int
    val: int

    def __len__(self):
        return self.end - self.start

def main(data):
    orig = []
    files = []
    spaces = []
    idx = 0
    full = True
    for char in data[0]:
        if full:
            files.append(DataRange(len(orig), len(orig)+int(char), idx))
            orig.extend(idx for _ in range(int(char)))
            idx += 1
        else:
            spaces.append(DataRange(len(orig), len(orig)+int(char), -1))
            orig.extend(-1 for _ in range(int(char)))
        full = not full

    # Star 1
    fragmented = orig.copy()
    left = 0
    right = len(fragmented) - 1
    while True:
        while fragmented[left] != -1:
            left += 1
        while fragmented[right] == -1:
            right -= 1
        if left < right:
            fragmented[left], fragmented[right] = fragmented[right], fragmented[left]
        else:
            break

    total = 0
    for idx, id_no in enumerate(fragmented):
        if id_no == -1:
            break
        total += idx*id_no
    print(total)

    # Star 2
    for file in reversed(files):
        for space in spaces:
            if space.start > file.start:
                break
            file_len = len(file)
            if file_len <= len(space):
                file.start = space.start
                file.end = space.start + file_len
                space.start = file.end
                break

    total = 0
    for file in files:
        total += sum(range(file.start, file.end)) * file.val
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
