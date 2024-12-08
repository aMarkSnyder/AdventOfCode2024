from collections import defaultdict

lines = []
with open('input.txt','r') as input:
    for line in input:
        lines.append(line.strip())

# Star 1
signals = defaultdict(list)
for row_idx, row in enumerate(lines):
    for col_idx, letter in enumerate(row):
        if letter != '.':
            signals[letter].append(row_idx + 1j * col_idx)

antinodes = defaultdict(set)
for letter, antennas in signals.items():
    for idx in range(len(antennas)):
        first = antennas[idx]
        for antenna in antennas[idx+1:]:
            dist = antenna - first
            antinodes[letter].add(antenna + dist)
            antinodes[letter].add(first - dist)

unique = set()
for letter_antinodes in antinodes.values():
    for antinode in letter_antinodes:
        if 0 <= antinode.real < len(lines) and 0 <= antinode.imag < len(lines):
            unique.add(antinode)
print(len(unique))

# Star 2
new_antinodes = defaultdict(set)
for letter, antennas in signals.items():
    new_antinodes[letter] = new_antinodes[letter].union(antennas)
    for idx in range(len(antennas)):
        first = antennas[idx]
        for antenna in antennas[idx+1:]:
            dist = antenna - first

            forward_node = antenna+dist
            while 0 <= forward_node.real < len(lines) and 0 <= forward_node.imag < len(lines):
                new_antinodes[letter].add(forward_node)
                forward_node += dist

            backward_node = first - dist
            while 0 <= backward_node.real < len(lines) and 0 <= backward_node.imag < len(lines):
                new_antinodes[letter].add(backward_node)
                backward_node -= dist

new_uniques = set()
for letter_antinodes in new_antinodes.values():
    new_uniques = new_uniques.union(letter_antinodes)
print(len(new_uniques))
