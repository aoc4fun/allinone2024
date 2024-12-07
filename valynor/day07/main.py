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

def compute_part1(result,data1,data2):
    if len(data2)==0:
        return data1==result
    else:
        return compute_part1(result,data1*data2[0],data2[1:]) or\
            compute_part1(result,data1+data2[0],data2[1:])

def compute_part2(result,data1,data2):
    if len(data2)==0:
        return data1==result
    else:
        return compute_part2(result,data1*data2[0],data2[1:]) or\
            compute_part2(result,data1+data2[0],data2[1:]) or\
            compute_part2(result,int(f"{str(data1)}{data2[0]}"),data2[1:])


def part1(lines):
    return sum(int(d[0]) for d in lines if compute_part1(int(d[0]),d[1][0],d[1][1:]))

def part2(lines):
    return sum(int(d[0]) for d in lines if compute_part2(int(d[0]),d[1][0],d[1][1:]))

assert_equal(part1(parse_data(sample)), 3749)
print(part1(parse_data(input_data)))

assert_equal(part2(parse_data(sample)), 11387)
print(part2(parse_data(input_data)))
