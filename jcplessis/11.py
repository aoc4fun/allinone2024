s="0 7 198844 5687836 58 2478 25475 894"

def blink(stones):
    res = []
    for stone in stones:
        if stone == 0:
            res.append(1)
        else:
            s = str(stone)
            if len(s) % 2 == 0:
                middle = int(len(s)/2)
                res.append(int(s[0:middle]))
                res.append(int(s[middle:len(s)]))
            else:
                res.append(stone*2024)
    return res

stones = list([int(x) for x in s.split()])
print(stones)
for i in range(25):
    print(i)
    stones = blink(stones)

print(len(stones))


cache = {}
def count(stone, depth):
    if depth == 0:
        return 1

    if (stone, depth) in cache:
        return cache[(stone, depth)]

    res = 0
    if stone == 0:
        res += count(1, depth-1)
    else:
        s = str(stone)
        if len(s) % 2 == 0:
            middle = int(len(s)/2)
            res += count(int(s[0:middle]), depth-1)
            res += count(int(s[middle:len(s)]), depth-1)
        else:
            res += count(stone*2024, depth-1)

    cache[(stone, depth)] = res

    return res

stones = list([int(x) for x in s.split()])
res = 0
for stone in stones:
    res += count(stone, 75)
    print(stone, res)

print(res)
