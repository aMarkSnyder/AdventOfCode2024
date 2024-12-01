# Star 1
l1 = []
l2 = []
with open('input.txt','r') as input:
    for line in input:
        digits = [int(num) for num in line.strip().split()]
        l1.append(digits[0])
        l2.append(digits[1])

l1 = sorted(l1)
l2 = sorted(l2)
dist = 0
for num1, num2 in zip(l1,l2):
    dist += abs(num1 - num2)
print(dist)

# Star 2
sim = 0
for num1 in l1:
    count = 0
    for num2 in l2:
        if num1 == num2:
            count += 1
    sim += count*num1
print(sim)