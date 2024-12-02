# Réflexion pendant 27 secondes
import os
from collections import Counter

def calculate_total_distance(left_list, right_list):
    # Sort both lists
    left_sorted = sorted(left_list)
    right_sorted = sorted(right_list)

    # Calculate pairwise distances and sum them up
    total_distance = sum(abs(l - r) for l, r in zip(left_sorted, right_sorted))
    return total_distance

def calculate_similarity_score(left_list, right_list):
    # Count occurrences of each number in the right list
    right_count = Counter(right_list)

    # Calculate similarity score
    similarity_score = sum(num * right_count[num] for num in left_list)
    return similarity_score

def read_input(file_path):
    with open(file_path, 'r') as file:
        left_list = []
        right_list = []
        for line in file:
            left, right = map(int, line.split())
            left_list.append(left)
            right_list.append(right)
    return left_list, right_list

# Test with sample data
sample_left = [3, 4, 2, 1, 3, 3]
sample_right = [4, 3, 5, 3, 9, 3]

# Part 1 Test
total_distance = calculate_total_distance(sample_left, sample_right)
print(f"Sample Total Distance: {total_distance}")  # Expected: 11

# Part 2 Test
similarity_score = calculate_similarity_score(sample_left, sample_right)
print(f"Sample Similarity Score: {similarity_score}")  # Expected: 31

# Read the input file and calculate answers
input_file = "01.txt"  # Replace with your actual input file path
if os.path.exists(input_file):
    left_list, right_list = read_input(input_file)

    # Part 1: Total Distance
    total_distance = calculate_total_distance(left_list, right_list)
    print(f"Total Distance: {total_distance}")

    # Part 2: Similarity Score
    similarity_score = calculate_similarity_score(left_list, right_list)
    print(f"Similarity Score: {similarity_score}")
else:
    print(f"Input file '{input_file}' not found.")
