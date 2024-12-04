sample="""MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX"""

with open("04.txt","r") as f:
    input_data=f.read()

objective="XMAS"

def parse_data(data):
    return [list(line) for line in data.split("\n")]

def check_in_direction_from(data,x,y,directionx,directiony,current_objective):
    for i in range(0,len(current_objective)):
        if x+i*directionx<0 or x+i*directionx>=len(data):
            return False
        if y+i*directiony<0 or y+i*directiony>=len(data[0]):
            return False
        if data[x+i*directionx][y+i*directiony]!=current_objective[i]:
            return False
    return True

def check_in_direction(data,directionx,directiony,current_objective):
    total=0
    for x in range(0,len(data)):
        for y in range(0,len(data[0])):
            if data[x][y]==current_objective[0]:
                total+=check_in_direction_from(data,x,y,directionx,directiony,current_objective)
    return total

def check_all_directions(data,current_objective):
    total=0
    for x in range(-1,2):
        for y in range(-1,2):
            if x!=0 or y!=0:
                total+=check_in_direction(data,x,y,current_objective)
    return total

def checkMAS(data):
    total=0
    for x in range(1,len(data)-1):
        for y in range(1,len(data[0])-1):
            if data[x][y]=="A" and ((data[x-1][y-1]=="M" and data[x+1][y+1]=="S") or (data[x-1][y-1]=="S" and data[x+1][y+1]=="M")) \
               and ((data[x+1][y-1]=="M" and data[x-1][y+1]=="S") or (data[x+1][y-1]=="S" and data[x-1][y+1]=="M")):
                   total=total+1
    return total

assert(check_all_directions(parse_data(sample),objective)==18)
print(f"Part 1 result : {checkMAS(parse_data(sample))}")

assert(checkMAS(parse_data(sample))==9)
print(f"Part 2 result : {checkMAS(parse_data(input_data))}")