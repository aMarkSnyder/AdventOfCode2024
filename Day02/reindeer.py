def test_safe(report):
    gaps = [report[idx] - report[idx-1] for idx in range(1, len(report))]
    num_level = len([gap for gap in gaps if gap == 0])
    num_up = len([gap for gap in gaps if gap > 0])
    num_down = len([gap for gap in gaps if gap < 0])
    max_gap = max(abs(gap) for gap in gaps)

    return (num_level == 0) and (max_gap < 4) and ((num_up == 0) or (num_down == 0))

lines = []
with open('input.txt','r') as input:
    for line in input:
        line = line.strip()
        lines.append([int(num) for num in line.split()])

safe = 0
kinda_safe = 0
for line_no, line in enumerate(lines):
    if test_safe(line):
        safe += 1
    else:
        for idx in range(len(line)):
            test_line = list(line)
            test_line.pop(idx)
            if test_safe(test_line):
                kinda_safe += 1
                break

print(safe)
print(safe+kinda_safe)
