import numpy as np

sample="""xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"""

with open("03.txt","r") as f:
    input_data=f.read()

import re
import functools

def extract_mul_and_sum_it_all(data):
    pattern = r"mul\((\d{1,3}),(\d{1,3})\)"
    matches = re.findall(pattern, data)
    return sum(functools.reduce(lambda a, b: a*b,(map(int, match))) for match in matches)

sample_2="xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))^don't()_mul(5,5)do()?mul(8,5)"

def extract_do_dont(data):
    pattern_extraction= r"do\(\)(.*?)don't\(\)"
    return "".join(re.findall(pattern_extraction, f"do(){data}don't()",re.DOTALL)) # re.DOTALL is used to match newlines

def extract_dont_do(data):
    pattern_extraction= r"don't\(\)(.*?)do\(\)"
    return "".join(re.findall(pattern_extraction, f"do(){data}don't()",re.DOTALL))

def part1(data):
    return extract_mul_and_sum_it_all(data)

def part2(data):
    return extract_mul_and_sum_it_all(extract_do_dont(data))

assert(part1(sample)==161)
print(f"Part 1 result : {part1(input_data)}")

assert(part2(sample_2)==88)
print(f"Part 2 result : {part2(input_data)}")