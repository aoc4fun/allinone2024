from PIL import Image, ImageDraw

def find_start_position(filename):
    # Read the file and create matrix
    with open(filename, 'r') as file:
        matrix = [list(line.strip()) for line in file]
    
    # Find the position of '^'
    for row in range(len(matrix)):
        for col in range(len(matrix[row])):
            if matrix[row][col] == '^':
                return (row, col)
    
    return None  # Return None if '^' is not found

def mark_path(filename):
    # Get start position
    matrix = []
    with open(filename, 'r') as file:
        matrix = [list(line.strip()) for line in file]
    
    start_row, start_col = find_start_position(filename)
    current_row, current_col = start_row, start_col
    
    # Direction vectors: [row_change, col_change]
    # Starting north, then east, south, west
    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    current_dir = 0  # Start moving north
    
    # Keep moving until we reach the edge
    while (0 <= current_row < len(matrix) and 
           0 <= current_col < len(matrix[0])):
        # Mark current position
        matrix[current_row][current_col] = 'X'
        
        # Calculate next position
        next_row = current_row + directions[current_dir][0]
        next_col = current_col + directions[current_dir][1]
        
        # Stop if we hit the edge
        if (next_row < 0 or next_row >= len(matrix) or 
            next_col < 0 or next_col >= len(matrix[0])):
            break
            
        # If we hit a wall, rotate 90° clockwise
        while(matrix[next_row][next_col] == '#'):
            current_dir = (current_dir + 1) % 4
            next_row = current_row + directions[current_dir][0]
            next_col = current_col + directions[current_dir][1]
        
        current_row, current_col = next_row, next_col
    
    return matrix

def count_x_marks(matrix):
    return sum(row.count('X') for row in matrix)

def create_grid_image(matrix, start_pos, cell_size=20):
    # Create an image with black background
    height = len(matrix) * cell_size
    width = len(matrix[0]) * cell_size
    image = Image.new('RGB', (width, height), 'black')
    draw = ImageDraw.Draw(image)
    
    # Colors for different cell types
    colors = {
        'X': 'green',
        '#': 'red',
        'L': 'blue',
    }
    
    # Draw each cell
    for row in range(len(matrix)):
        for col in range(len(matrix[0])):
            x1 = col * cell_size
            y1 = row * cell_size
            x2 = x1 + cell_size
            y2 = y1 + cell_size
            
            cell = matrix[row][col]
            if cell in colors:
                draw.rectangle([x1, y1, x2, y2], fill=colors[cell])
    
    # Draw starting position in yellow
    start_row, start_col = start_pos
    x1 = start_col * cell_size
    y1 = start_row * cell_size
    x2 = x1 + cell_size
    y2 = y1 + cell_size
    draw.rectangle([x1, y1, x2, y2], fill='yellow')
                
    # Save the image
    image.save('grid.png')

def is_infinite_loop(matrix, start_pos, test_row, test_col):
    # Create a copy of the matrix for testing
    test_matrix = [row[:] for row in matrix]
    test_matrix[test_row][test_col] = '#'
    
    # Track visited positions and their directions
    visited = set()
    current_row, current_col = start_pos
    current_dir = 0  # Start moving north
    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    
    while True:
        # Create a state tuple (position and direction)
        state = (current_row, current_col, current_dir)
        
        # If we've seen this state before, it's a loop
        if state in visited:
            return True
        
        # If we're out of bounds, it's not a loop
        if (current_row < 0 or current_row >= len(test_matrix) or 
            current_col < 0 or current_col >= len(test_matrix[0])):
            return False
            
        visited.add(state)
        
        # Calculate next position
        next_row = current_row + directions[current_dir][0]
        next_col = current_col + directions[current_dir][1]
        
        # If we hit the edge
        if (next_row < 0 or next_row >= len(test_matrix) or 
            next_col < 0 or next_col >= len(test_matrix[0])):
            return False
            
        # If we hit a wall, rotate 90° clockwise
        while(test_matrix[next_row][next_col] == '#'):
            current_dir = (current_dir + 1) % 4
            next_row = current_row + directions[current_dir][0]
            next_col = current_col + directions[current_dir][1]
        
        current_row, current_col = next_row, next_col

def find_loop_positions(filename):
    # Get start position and matrix
    matrix = []
    with open(filename, 'r') as file:
        matrix = [list(line.strip()) for line in file]
    
    start_pos = find_start_position(filename)
    current_row, current_col = start_pos
    loop_positions = set()
    
    # Direction vectors
    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    current_dir = 0  # Start moving north
    
    # Keep moving until we reach the edge
    while (0 <= current_row < len(matrix) and 
           0 <= current_col < len(matrix[0])):
        
        # Calculate next position
        next_row = current_row + directions[current_dir][0]
        next_col = current_col + directions[current_dir][1]
        
        # Stop if we hit the edge
        if (next_row < 0 or next_row >= len(matrix) or 
            next_col < 0 or next_col >= len(matrix[0])):
            break
            
        
        # If we hit a wall, rotate 90° clockwise
        while(matrix[next_row][next_col] == '#'):
            current_dir = (current_dir + 1) % 4
            next_row = current_row + directions[current_dir][0]
            next_col = current_col + directions[current_dir][1]

        # Test if placing a wall here would create a loop
        if (next_row, next_col) != start_pos and is_infinite_loop(matrix, start_pos, next_row, next_col):
            loop_positions.add((next_row, next_col))


        current_row, current_col = next_row, next_col
    
    return loop_positions

# Test the function
if __name__ == "__main__":
    start_pos = find_start_position('02.txt')
    print(f"Start position (row, col): {start_pos}")
    
    # Find all positions that would create loops
    loop_positions = find_loop_positions('02.txt')
    print(f"\nNumber of positions that create loops: {len(loop_positions)}")
    
    # Create the normal path visualization
    modified_matrix = mark_path('02.txt')
    
    # Mark loop positions with a different color in the visualization
    for row, col in loop_positions:
        modified_matrix[row][col] = 'L'  # Mark loop positions
    
    # Print the text version
    for row in modified_matrix:
        print(''.join(row))
    
    # Generate the image
    create_grid_image(modified_matrix, start_pos)
    print("\nGrid image saved as 'grid.png'")
