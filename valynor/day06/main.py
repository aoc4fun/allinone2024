def parse_map(input_map):
    grid = [list(row) for row in input_map.strip().split("\n")]
    directions = {'^': (-1, 0), 'v': (1, 0), '<': (0, -1), '>': (0, 1)}
    guard_pos, guard_dir = None, None

    for r, row in enumerate(grid):
        for c, cell in enumerate(row):
            if cell in directions:
                guard_pos = (r, c)
                guard_dir = cell
                grid[r][c] = '.'  # Replace guard with empty space
                break
        if guard_pos:
            break

    return grid, guard_pos, guard_dir, directions


def move_guard(grid, pos, direction, directions, obstruction):
    rows, cols = len(grid), len(grid[0])
    dr, dc = directions[direction]
    nr, nc = pos[0] + dr, pos[1] + dc

    # Allow moving out of bounds
    if 0 <= nr < rows and 0 <= nc < cols:
        if (nr, nc) != obstruction and grid[nr][nc] == '.':
            return (nr, nc), direction  # Move forward
    else:
        # If out of bounds, consider the guard as having left the grid
        return (nr, nc), direction

    # If blocked, turn right
    new_dir = {'^': '>', '>': 'v', 'v': '<', '<': '^'}[direction]
    return pos, new_dir


def simulate_path(grid, start_pos, start_dir, directions, obstruction):
    visited = set()
    pos, direction = start_pos, start_dir

    while (pos, direction) not in visited:
        visited.add((pos, direction))
        pos, direction = move_guard(grid, pos, direction, directions, obstruction)
        # Stop if the guard leaves the grid
        if not (0 <= pos[0] < len(grid) and 0 <= pos[1] < len(grid[0])):
            return False  # Guard leaves the map

    return True  # Guard is stuck in a loop

import time
def count_loop_positions(input_map):
    grid, guard_pos, guard_dir, directions = parse_map(input_map)
    rows, cols = len(grid), len(grid[0])
    loop_positions = 0
    total = rows * cols
    progress_step = 50  # Length of the progress bar
    start_time = time.time()

    for r in range(rows):
        for c in range(cols):
            current = r * cols + c + 1
            progress = int((current / total) * progress_step)
            bar = '[' + '*' * progress + '.' * (progress_step - progress) + ']'

            # Calculate elapsed time
            elapsed_time = time.time() - start_time
            elapsed_str = f"{elapsed_time:.2f}s"

            print(f"\r{bar} {current}/{total} Elapsed: {elapsed_str}", end="")
            if grid[r][c] == '.' and (r, c) != guard_pos:
                # Simulate with a virtual obstruction at (r, c)
                if simulate_path(grid, guard_pos, guard_dir, directions, (r, c)):
                    loop_positions += 1
    print()
    return loop_positions


# Example Input
sample_map = """
....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...
"""

# Run the function

with open("06.txt", "r") as f:
    input_map = f.read()

assert(count_loop_positions(sample_map)==6)

result = count_loop_positions(input_map)
print("Number of positions to cause a loop:", result)
