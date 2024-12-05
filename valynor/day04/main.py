import itertools

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
        if x+i*directionx<0 or x+i*directionx>=len(data) or\
            y+i*directiony<0 or y+i*directiony>=len(data[0]) or \
            data[x + i * directionx][y + i * directiony] != current_objective[i]:
            return False
    return True

def check_in_direction(data,directionx,directiony,current_objective):
    return sum(check_in_direction_from(data, x, y, directionx, directiony, current_objective)
               for (x,y) in list(itertools.product(range(0,len(data)), range(0,len(data[0]))))
               if data[x][y]==current_objective[0])

def check_all_directions(data,current_objective):
    combinaison=list(itertools.product(range(-1,2), range(-1,2)))
    combinaison.remove((0,0))
    return sum(
        check_in_direction(data,x,y,current_objective)
        for x,y in combinaison
    )

def checkMAS(data):
    return sum(
        [
            data[x][y]=="A" and
            ((data[x-1][y-1]=="M" and data[x+1][y+1]=="S") or
             (data[x-1][y-1]=="S" and data[x+1][y+1]=="M")) and
            ((data[x+1][y-1]=="M" and data[x-1][y+1]=="S") or
             (data[x+1][y-1]=="S" and data[x-1][y+1]=="M"))
            for x,y in list(itertools.product( range(1,len(data)-1), range(1,len(data[0])-1)))
        ]
    )

assert(check_all_directions(parse_data(sample),objective)==18)
print(f"Part 1 result : {check_all_directions(parse_data(input_data),objective)}")

assert(checkMAS(parse_data(sample))==9)
print(f"Part 2 result : {checkMAS(parse_data(input_data))}")