def load_file_into_matrix(filename):
    matrix = []
    with open(filename, 'r') as file:
        for line in file:
            matrix.append(list(line.strip()))
    return matrix

def find_special_A(matrix):
    rows = len(matrix)
    cols = len(matrix[0]) if rows > 0 else 0
    special_a_positions = []

    # Directions for diagonals (both ways)
    directions = [
        [(-1, 1), (0, 0), (1, -1)],  # top-right to bottom-left and vice versa
        [(-1, -1), (0, 0), (1, 1)]   # top-left to bottom-right and vice versa
    ]

    for row in range(rows):
        for col in range(cols):
            if matrix[row][col] == 'A':  # Found an A
                (dir1, dir2) = directions
                if (check_diagonal_word(matrix, row, col, dir1, "MAS") or check_diagonal_word(matrix, row, col, dir1, "SAM")) and \
                    (check_diagonal_word(matrix, row, col, dir2, "SAM") or check_diagonal_word(matrix, row, col, dir2, "MAS")):
                        special_a_positions.append((row, col))
    return special_a_positions

def check_diagonal_word(matrix, start_row, start_col, direction, word):
    rows = len(matrix)
    cols = len(matrix[0])
    word_length = len(word)
    for k in range(word_length):
        nr = start_row + direction[k][0]
        nc = start_col + direction[k][1]
        if not (0 <= nr < rows and 0 <= nc < cols):
            return False
        if matrix[nr][nc] != word[k]:
            return False
    return True

# Usage example:
matrix = load_file_into_matrix('04.txt')
positions = find_special_A(matrix)

# Print the positions where the special 'A' is found
for position in positions:
    print(f'Special "A" found at {position}')

print(len(positions))
