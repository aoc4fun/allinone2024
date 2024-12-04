import re

# Read the content of the file
with open('03.txt', 'r') as file:
    text = file.read()

# Updated regular expression pattern to match:
# - "mul(X, Y)" where X and Y are between 0 and 999 with no spaces after the comma
# - "do()"
# - "don't()"
pattern = r"(mul\((\d{1,3}),(\d{1,3})\)|do\(\)|don't\(\))"

# Find all matches in the text
matches = re.findall(pattern, text)

# List to store the results of the multiplications
multiplications = []

# Flag to track whether we should ignore multiplications
ignore_multiplications = False

# Process each match
for match in matches:
    full_match = match[0]

    if full_match == "don't()":
        ignore_multiplications = True
        print(f"Found: don't() - Start ignoring multiplications")
    elif full_match == "do()":
        ignore_multiplications = False
        print(f"Found: do() - Stop ignoring multiplications")
    elif full_match.startswith("mul"):
        if not ignore_multiplications:
            x, y = map(int, match[1:3])  # Extract the captured numeric groups and convert to integers
            if 0 <= x <= 999 and 0 <= y <= 999:
                result = x * y
                multiplications.append(result)
                print(f"Found: mul({x}, {y}), multiplication: {result}")
        else:
            x, y = map(int, match[1:3])
            print(f"Found but ignored: mul({x}, {y})")

# Compute the sum of all multiplications
total_sum = sum(multiplications)

# Print the total sum
print(f"Sum of all multiplications: {total_sum}")
