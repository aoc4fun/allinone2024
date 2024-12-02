import numpy as np

sample="""7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9"""

with open("02.txt","r") as f:
    input_data=f.read()

def parse_data(data):
    return [list(map(int, line.split())) for line in data.split("\n")]

def distance(d1,d2,min,max):
    return min <= d1-d2 <=max

# Part 1
def check_increasing_unboundlimit(level,min=1,max=3):
    return all(distance(level[i],level[i+1],min,max) for i in range(len(level)-1))

def is_safe(level):
    return check_increasing_unboundlimit(level) or check_increasing_unboundlimit(level[::-1])

def part1(data):
    return len([line for line in parse_data(data) if is_safe(line)])

# Part 2
def extract_others_lists(data):
    return [[data[i] for i in range(0,len(data)) if i!=extract] for extract in range(0,len(data))]

def part2(data):
    return len([1 for line in parse_data(data) if any([is_safe(list_to_check) for list_to_check in extract_others_lists(line)])])

assert(part1(sample)==2)
print(f"Part 1 result : {part1(input_data)}")

assert(part2(sample)==4)
print(f"Part 1 result : {part2(input_data)}")