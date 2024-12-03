import re
from math import prod

def eval_instr(mul_instr):
    pattern = r"\d+"
    nums = re.findall(pattern, mul_instr)
    return prod(int(num) for num in nums)

lines = []
with open('input.txt','r') as input:
    for line in input:
        lines.append(line.strip())

# Star 1
pattern = r"mul\(\d{1,3},\d{1,3}\)"
matches = []
for line in lines:
    matches.extend(re.findall(pattern, line))

print(sum(eval_instr(mul_instr) for mul_instr in matches))

# Star 2
pattern = r"mul\(\d{1,3},\d{1,3}\)|do\(\)|don't\(\)"
matches = []
for line in lines:
    matches.extend(re.findall(pattern, line))

enabled = True
total = 0
for match in matches:
    if match == "do()":
        enabled = True
    elif match == "don't()":
        enabled = False
    else:
        if enabled:
            total += eval_instr(match)

print(total)