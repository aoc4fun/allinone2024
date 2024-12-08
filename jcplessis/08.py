from PIL import Image, ImageDraw, ImageFont

def load_map(filename):
    # Read the file and create matrix
    with open(filename, 'r') as file:
        matrix = [list(line.strip()) for line in file]
    return matrix

def find_distinct_chars(matrix):
    # Create a set of all characters (excluding dots)
    chars = set()
    for row in matrix:
        for char in row:
            if char != '.':
                chars.add(char)
    return sorted(list(chars))  # Convert to sorted list for consistent output

def find_char_locations(matrix, chars):
    # Dictionary to store locations for each character
    locations = {}
    
    # Initialize empty list for each character
    for char in chars:
        locations[char] = []
    
    # Find all locations
    for row in range(len(matrix)):
        for col in range(len(matrix[row])):
            char = matrix[row][col]
            if char != '.':
                locations[char].append((row, col))
    
    return locations

def find_symmetrical_positions(locations, matrix):
    symmetrical_positions = {}
    rows = len(matrix)
    cols = len(matrix[0])
    
    # For each character and its locations
    for char, points in locations.items():
        symmetrical_positions[char] = []
        
        # For each pair of points
        for i in range(len(points)):
            for j in range(len(points)):
                if i != j:  # Don't pair a point with itself
                    p1 = points[i]  # First point
                    p2 = points[j]  # Second point
                    
                    # Calculate the direction vector from p1 to p2
                    delta_row = p2[0] - p1[0]
                    delta_col = p2[1] - p1[1]
                    
                    # Keep applying the same vector starting from p2
                    current_point = p1
                    while True:
                        # Calculate next position using the same vector
                        next_row = current_point[0] + delta_row
                        next_col = current_point[1] + delta_col
                        
                        # Check if we're still within bounds
                        if (0 <= next_row < rows and 
                            0 <= next_col < cols):
                            symmetrical_positions[char].append({
                                'point1': p1,
                                'center': p2,
                                'symmetrical': (next_row, next_col)
                            })
                            # Continue with next iteration from this point
                            current_point = (next_row, next_col)
                        else:
                            break  # Stop when we reach the boundary
    
    return symmetrical_positions

def create_map_image(matrix, symmetrical_positions, cell_size=20):
    # Create an image with black background
    height = len(matrix) * cell_size
    width = len(matrix[0]) * cell_size
    image = Image.new('RGB', (width, height), 'black')
    draw = ImageDraw.Draw(image)
    
    # Try to load a font, fall back to default if not found
    try:
        font = ImageFont.truetype("arial.ttf", int(cell_size * 0.8))
    except:
        font = ImageFont.load_default()
    
    # First draw red backgrounds for symmetrical positions
    for char, positions in symmetrical_positions.items():
        for pos in positions:
            sym_row, sym_col = pos['symmetrical']
            x1 = sym_col * cell_size
            y1 = sym_row * cell_size
            x2 = x1 + cell_size
            y2 = y1 + cell_size
            draw.rectangle([x1, y1, x2, y2], fill='red')
    
    # Then draw characters in yellow on top
    for row in range(len(matrix)):
        for col in range(len(matrix[0])):
            char = matrix[row][col]
            if char != '.':
                x = col * cell_size
                y = row * cell_size
                # Center the text in the cell
                char_bbox = draw.textbbox((0, 0), char, font=font)
                char_width = char_bbox[2] - char_bbox[0]
                char_height = char_bbox[3] - char_bbox[1]
                x += (cell_size - char_width) // 2
                y += (cell_size - char_height) // 2
                draw.text((x, y), char, fill='yellow', font=font)
    
    # Save the image
    image.save('map.png')

def count_symmetrical_points(symmetrical_positions):
    # Set to store unique symmetrical positions
    unique_positions = set()
    
    # Add all symmetrical positions to the set
    for char, positions in symmetrical_positions.items():
        for pos in positions:
            unique_positions.add(pos['symmetrical'])
    
    return len(unique_positions)

if __name__ == "__main__":
    # Load the map
    matrix = load_map('08.txt')
    
    # Find distinct characters
    distinct_chars = find_distinct_chars(matrix)
    print("Distinct characters found:")
    print(distinct_chars)
    print(f"Total count: {len(distinct_chars)}")
    
    # Find locations for each character
    locations = find_char_locations(matrix, distinct_chars)
    
    # Find symmetrical positions
    symmetrical_positions = find_symmetrical_positions(locations, matrix)
    
    # Create visualization
    create_map_image(matrix, symmetrical_positions)
    print("\nMap image saved as 'map.png'")
    
    # Count and print total unique symmetrical points
    total_symmetrical = count_symmetrical_points(symmetrical_positions)
    print(f"\nTotal number of unique symmetrical points: {total_symmetrical}")
