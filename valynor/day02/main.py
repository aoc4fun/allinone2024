import numpy as np

sample="""7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9"""

with open("02.txt","r") as f:
    inputdata=f.read()

def parse_data(data):
    input_data=[]
    for line in data.split("\n"):
        input_data.append((list(map(int, line.split()))))
    #input_data = np.array([list(map(int, line.split())) for line in data.split("\n")])
    return input_data

def distance(d1,d2):
    return 0<(d1-d2)<4

# Part 1
def check_upper(line):
    for i in range(len(line)-1):
        if not distance(line[i],line[i+1]):
            return False
    return True

def part1(data):
    return len([line for line in parse_data(data) if check_upper(line) or check_upper(line[::-1])])

# Part 2
def extract_list(data):
    lists=[data]
    for extract in range(0,len(data)):
        current_list=[]
        for i in range(0,len(data)):
            if i!=extract:
                current_list.append(data[i])
        lists.append(current_list)
    return lists

def part2(data):
    counter=0
    for line in parse_data(data):
        list_trying=extract_list(line)
        list_trying2=extract_list(line[::-1])
        joined_list=[*list_trying,*list_trying2]
        for list_to_check in joined_list:
            if check_upper(list_to_check):
                counter+=1
                break
    return counter

assert(part1(sample)==2)
print(f"Part 1 result : {part1(inputdata)}")

assert(part2(sample)==4)
print(f"Part 1 result : {part2(inputdata)}")