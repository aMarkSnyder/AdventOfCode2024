from collections import defaultdict

lines = []
with open('input.txt','r') as input:
    for line in input:
        lines.append(line.strip())

rules = defaultdict(set)
for idx, line in enumerate(lines):
    if line == '':
        break
    left, right = line.split('|')
    rules[left].add(right)
updates = [line.split(',') for line in lines[idx+1:]]

def swap_first_error(rules, update):
    seen = {}
    found_error = False
    for idx, page in enumerate(update):
        if page not in seen:
            seen[page] = idx
        if page in rules:
            for rule_page in rules[page]:
                if rule_page in seen:
                    left_idx = seen[rule_page]
                    right_idx = idx
                    found_error = True
                    break
        if found_error:
            break
    if found_error:
        update[left_idx], update[right_idx] = update[right_idx], update[left_idx]
    return found_error

# Star 1
total = 0
wrong_updates = []
for update in updates:
    seen = set()
    valid = True
    for page in update:
        if page in rules and any(pp in seen for pp in rules[page]):
            valid = False
            wrong_updates.append(update)
            break
        seen.add(page)
    if valid:
        total += int(update[len(update)//2])
print(total)

# Star 2
total = 0
for update in wrong_updates:
    while(swap_first_error(rules, update)):
        pass
    total += int(update[len(update)//2])
print(total)