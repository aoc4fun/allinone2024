from numpy.ma.testutils import assert_equal

sample="""190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20"""

with open("07.txt","r") as f:
    input_data=f.read()

def parse_data(input_data):
    return [(line.split(":")[0],list(map(int, line.split(":")[1].split()))) for line in input_data.split("\n")]


def compute(result, data, allow_concat=False):
    def helper(current, remaining):
        if not remaining:
            return current == result
        next_val = remaining[0]
        rest = remaining[1:]

        if helper(current * next_val, rest):
            return True
        if helper(current + next_val, rest):
            return True

        if allow_concat:
            concat_val = int(str(current) + str(next_val))
            if helper(concat_val, rest):
                return True

        return False

    return helper(data[0], data[1:])


def part1(lines):
    return sum(int(d[0]) for d in lines if compute(int(d[0]),d[1], False))

def part2(lines):
    return sum(int(d[0]) for d in lines if compute(int(d[0]),d[1], True))

assert_equal(part1(parse_data(sample)), 3749)
print(f"result part1 : {part1(parse_data(input_data))}")

assert_equal(part2(parse_data(sample)), 11387)
print(f"result part1 : {part2(parse_data(input_data))}")
