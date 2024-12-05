# Initialize the lists
rules = []
updates = []

# Open and read the file
with open('05.txt', 'r') as file:
    content = file.read()


# Split the content into two parts based on the blank line
parts = content.split('\n\n')

# Process the rules part
if len(parts) > 0:
    rules_lines = parts[0].strip().split('\n')
    for line in rules_lines:
        number1, number2 = line.split('|')
        rules.append((int(number1.strip()), int(number2.strip())))

# Process the updates part
if len(parts) > 1:
    updates_lines = parts[1].strip().split('\n')
    for line in updates_lines:
        updates.append([int(number) for number in line.split(',')])

# Function to check if a single update is valid
def is_update_valid(rules, update):
    seen = set()

    for number in update:
        for rule in rules:
            if rule[0] == number:
                if rule[1] in seen:
                    return False
        seen.add(number)

    return True

# List to hold all valid updates
valid_updates = []
# List to hold all invalid updates
invalid_updates = []

# Iterate through each update and validate it
for update in updates:
    if is_update_valid(rules, update):
        valid_updates.append(update)
    else:
        invalid_updates.append(update)

# Function to fix an invalid update by swapping the broken rules
def fix_update(rules, update):
    while not is_update_valid(rules, update):
        seen = set()
        for i, number in enumerate(update):
            for rule in rules:
                if rule[0] == number and rule[1] in seen:
                    # Swap the number and recheck
                    update[i], update[i - 1] = update[i - 1], update[i]
                    break
            seen.add(number)
    return update

# Fix the invalid updates
fixed_updates = [fix_update(rules, list(update)) for update in invalid_updates]

# Print the fixed updates
print("Fixed Updates:", fixed_updates)

# Calculate the sum of the middle number for each valid update
def calculate_middle_sum(updates):
    middle_sum = 0
    for update in updates:
        if len(update) % 2 == 1:
            middle_index = len(update) // 2
            middle_sum += update[middle_index]
    return middle_sum

# Sum of middle numbers for all updates
total_middle_sum_valid = calculate_middle_sum(valid_updates)
total_middle_sum_fixed = calculate_middle_sum(fixed_updates)

# Print the results
print("Sum of middle numbers for valid updates:", total_middle_sum_valid)
print("Sum of middle numbers for fixed updates:", total_middle_sum_fixed)
print("Total sum of middle numbers:", total_middle_sum_valid + total_middle_sum_fixed)
