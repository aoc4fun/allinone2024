import numpy as np

sample="""3   4
4   3
2   5
1   3
3   9
3   3"""
with open("01.txt","r") as f:
    puzzle_input=f.read()

def parse_data(puzzle_input):
    input_data = np.array([list(map(int, line.split())) for line in puzzle_input.split("\n")])
    return sorted(input_data.T[0]), sorted(input_data.T[1])

def total_distance_1(puzzle_input):
    return sum([abs(i-j) for (i,j) in zip(*parse_data(puzzle_input))])

# Part 1
assert(total_distance_1(sample)==11)
print(total_distance_1(data))

def total_distance_2(puzzle_input):
    first,second=parse_data(puzzle_input)
    return sum([i*second.count(i) for i in first])

# Part 2
assert(total_distance_2(sample)==31)
print(total_distance_2(puzzle_input))