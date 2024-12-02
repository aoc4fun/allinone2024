# Réflexion pendant 26 secondes

import sys

with open("02.txt","r") as f:
    input_data=f.read()

sample="""7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9"""

def is_safe(levels):
    # Check if the levels are strictly increasing or strictly decreasing
    increasing = all(levels[i] > levels[i-1] for i in range(1, len(levels)))
    decreasing = all(levels[i] < levels[i-1] for i in range(1, len(levels)))
    if not (increasing or decreasing):
        return False
    # Check if adjacent differences are between 1 and 3 inclusive
    diffs = [abs(levels[i] - levels[i-1]) for i in range(1, len(levels))]
    return all(1 <= diff <= 3 for diff in diffs)

def can_be_made_safe(levels):
    for i in range(len(levels)):
        new_levels = levels[:i] + levels[i+1:]
        if is_safe(new_levels):
            return True
    return False

safe_reports = 0
can_be_safe = 0
for line in input_data.split("\n"):
    levels = list(map(int, line.strip().split()))
    if not levels:
        continue
    if is_safe(levels):
        safe_reports += 1
    elif can_be_made_safe(levels):
        can_be_safe += 1

print(safe_reports)
print(safe_reports+can_be_safe)
