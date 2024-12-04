def load_file_into_matrix(filename):
    matrix = []
    with open(filename, 'r') as file:
        for line in file:
            matrix.append(list(line.strip()))
    return matrix

def find_word_in_matrix(matrix, word):
    rows = len(matrix)
    cols = len(matrix[0]) if rows > 0 else 0
    word_length = len(word)
    occurrences = []

    # Directions: right, left, down, up, down-right, down-left, up-right, up-left
    directions = [
        (0, 1),  # right
        (0, -1),  # left
        (1, 0),  # down
        (-1, 0),  # up
        (1, 1),  # down-right
        (1, -1),  # down-left
        (-1, 1),  # up-right
        (-1, -1),  # up-left
    ]

    for row in range(rows):
        for col in range(cols):
            if matrix[row][col] == word[0]:  # Found the starting letter
                for dr, dc in directions:  # Check all eight directions
                    found = True
                    for k in range(word_length):
                        nr, nc = row + dr * k, col + dc * k  # Calculate new position
                        if (0 <= nr < rows and 0 <= nc < cols):  # Check boundaries
                            if matrix[nr][nc] != word[k]:
                                found = False
                                break
                        else:
                            found = False
                            break
                    if found:
                        occurrences.append((row, col))

    return occurrences

# Usage example:
matrix = load_file_into_matrix('04.txt')
word = "XMAS"
positions = find_word_in_matrix(matrix, word)

# Print the positions where "XMAS" is found
for position in positions:
    print(f'Word "{word}" found starting at {position}')

print(len(positions))
