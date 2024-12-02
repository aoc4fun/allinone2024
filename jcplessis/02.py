with open('02.txt', 'r') as file:
    # Read each line from the file
    lines = file.readlines()

# Initialize counters for lines with all positive or all negative differences within the range [-3, 3]
positive_diff_in_range_count = 0
negative_diff_in_range_count = 0

def check_differences(numbers):
    differences = [numbers[i + 1] - numbers[i] for i in range(len(numbers) - 1)]
    if all(-3 <= diff <= 3 for diff in differences):
        if all(diff > 0 for diff in differences):
            return "positive"
        elif all(diff < 0 for diff in differences):
            return "negative"
    return None

for line in lines:
    line = line.strip()
    numbers = [int(num) for num in line.split()]

    result = check_differences(numbers)
    if result == "positive":
        positive_diff_in_range_count += 1
    elif result == "negative":
        negative_diff_in_range_count += 1
    else:
        # If the line does not match the rules, try removing each number one at a time
        for i in range(len(numbers)):
            temp_numbers = numbers[:i] + numbers[i+1:]
            result = check_differences(temp_numbers)
            if result == "positive":
                positive_diff_in_range_count += 1
                break
            elif result == "negative":
                negative_diff_in_range_count += 1
                break

# Print the counts
print(f'Lines with all positive differences in the range [-3, 3]: {positive_diff_in_range_count}')
print(f'Lines with all negative differences in the range [-3, 3]: {negative_diff_in_range_count}')

print(positive_diff_in_range_count + negative_diff_in_range_count)
