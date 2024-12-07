lines = []
with open('input.txt','r') as input:
    for line in input:
        lines.append(line.strip())

def valid_equation(result, numbers):
    if len(numbers) == 1:
        return result == numbers[0]
    if result < numbers[0]:
        return False
    added_numbers = [numbers[0]+numbers[1]] + numbers[2:]
    multiplied_numbers = [numbers[0]*numbers[1]] + numbers[2:]
    if valid_equation(result, added_numbers) or valid_equation(result, multiplied_numbers):
        return True
    
def valid_concat_equation(result, numbers):
    if len(numbers) == 1:
        return result == numbers[0]
    if result < numbers[0]:
        return False
    added_numbers = [numbers[0]+numbers[1]] + numbers[2:]
    multiplied_numbers = [numbers[0]*numbers[1]] + numbers[2:]
    concat_numbers = [int(str(numbers[0])+str(numbers[1]))] + numbers[2:]
    if valid_concat_equation(result, added_numbers) or valid_concat_equation(result, multiplied_numbers) or valid_concat_equation(result, concat_numbers):
        return True

# Star 1
equations = {}
for line in lines:
    result, numbers = line.split(': ')
    result = int(result)
    numbers = [int(number) for number in numbers.strip().split()]
    equations[result] = numbers

valid = set()
for result, numbers in equations.items():
    if valid_equation(result, numbers):
        valid.add(result)
print(sum(valid))

# Star 2
invalid = set(equations) - valid
for result in invalid:
    if valid_concat_equation(result, equations[result]):
        valid.add(result)
print(sum(valid))
