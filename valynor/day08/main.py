import matplotlib.pyplot as plt
from math import gcd

def read_map_from_file(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        lines = [line.rstrip('\n') for line in f]
    return lines

def find_antenna(antennas_map):
    rows = len(antennas_map)
    cols = len(antennas_map[0]) if rows > 0 else 0
    freq_positions = {}
    for r in range(rows):
        for c in range(cols):
            ch = antennas_map[r][c]
            if ch != '.':
                freq_positions.setdefault(ch, []).append((r, c))
    return freq_positions


import itertools
def find_antinodes_part1(antennas_positions, maps_size):
    antinodes = set()

    for freq, positions in antennas_positions.items():
        n = len(positions)
        for i in range(n):
            for j in range(i + 1, n):
                r1, c1 = positions[i]
                r2, c2 = positions[j]

                dr = r2 - r1
                dc = c2 - c1

                A1_r = r1 - dr
                A1_c = c1 - dc

                A2_r = r2 + dr
                A2_c = c2 + dc

                # Check if antinodes are within the map
                if 0 <= A1_r < maps_size[0] and 0 <= A1_c < maps_size[1]:
                    antinodes.add((A1_r, A1_c))
                if 0 <= A2_r < maps_size[0] and 0 <= A2_c < maps_size[1]:
                    antinodes.add((A2_r, A2_c))

    return antinodes

def find_antinodes_part2(antennas_positions, maps_size):

    antinodes = set()

    for freq, positions in antennas_positions.items():
        n = len(positions)
        if n < 2:
            # Only one antenna of this frequency, no line can be formed
            continue
        # Consider all pairs
        for i in range(n):
            for j in range(i+1, n):
                r1, c1 = positions[i]
                r2, c2 = positions[j]

                dr = r2 - r1
                dc = c2 - c1
                g = gcd(dr, dc)
                dr //= g
                dc //= g

                # Move backward
                rr, cc = r1, c1
                while True:
                    nr = rr - dr
                    nc = cc - dc
                    if 0 <= nr < maps_size[0] and 0 <= nc < maps_size[1]:
                        rr, cc = nr, nc
                    else:
                        break

                # Now go forward from rr, cc along (dr, dc), adding all points inside bounds
                while 0 <= rr < maps_size[0] and 0 <= cc < maps_size[1]:
                    antinodes.add((rr, cc))
                    rr += dr
                    cc += dc

    return antinodes

def plot_solution(antennas_map, antinodes, freq_positions, output_png="solution.png"):
    rows = len(antennas_map)
    cols = len(antennas_map[0]) if rows > 0 else 0

    fig, ax = plt.subplots(figsize=(max(cols/2, 4), max(rows/2, 4)))
    ax.set_xlim(-0.5, cols - 0.5)
    ax.set_ylim(rows - 0.5, -0.5)
    ax.set_aspect('equal')

    # Plot antennas
    for r in range(rows):
        for c in range(cols):
            ch = antennas_map[r][c]
            if ch != '.':
                ax.plot(c, r, 'o', color='black', markersize=10)
                ax.text(c, r, ch, ha='center', va='center', color='white', fontsize=8, fontweight='bold')

    # Plot antinodes as red '+'
    for (r, c) in antinodes:
        # If there's already an antenna, mark over it anyway
        ax.plot(c, r, '+', color='red', markersize=10, markeredgewidth=2)

    ax.set_xticks(range(cols))
    ax.set_yticks(range(rows))
    ax.grid(True, which='both', linestyle=':', color='gray')
    ax.invert_yaxis()

    plt.tight_layout()
    plt.savefig(output_png, dpi=150)
    # plt.show()

from PIL import Image, ImageDraw, ImageFont

def plot_pil(antennas_position, antinodes_part1,maps_size,output_png="solution.png"):
    font = ImageFont.load_default()

    # Determine the image size needed for the text
    max_width = maps_size[0]
    max_height = maps_size[1]

    padding = 10
    cell_size = 20
    img_width = max_width * cell_size
    img_height = max_height * cell_size

    # Create a white background image
    img = Image.new("RGB", (img_width, img_height), "white")
    draw = ImageDraw.Draw(img)
    font = ImageFont.load_default()

    # Draw a light gray grid
    for r in range(max_width + 1):
        draw.line((0, r * cell_size, img_width, r * cell_size), fill="lightgray")
    for c in range(max_height + 1):
        draw.line((c * cell_size, 0, c * cell_size, img_height), fill="lightgray")

    # Draw antennas based on freq_positions
    for positions in antinodes_part1:
            r, c = positions
            x = c * cell_size
            y = r * cell_size
            # Draw a black rectangle for the antenna cell
            draw.rectangle([x, y, x+cell_size, y+cell_size], fill="red")

    for freq, positions in antennas_position.items():
        for (r, c) in positions:
            x = c * cell_size
            y = r * cell_size
            # Draw a black rectangle for the antenna cell
            #draw.rectangle([x, y, x+cell_size, y+cell_size], fill="black")
            # Draw the frequency character in the center
            # Calculate text width and height using the font metrics
            _,_,w, h = font.getbbox(freq)  # or use font.getbbox(freq) for more accurate bounding box

            text_x = x + (cell_size - w) / 2
            text_y = y + (cell_size - h) / 2

            draw.text((text_x, text_y), freq, fill="black", font=font)

    # Save the resulting image
    img.save(output_png)
    print(f"Saved antenna map to {output_png}")

sample="""............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............"""

input_file = "08.txt"

# Read the input map
antennas_map = read_map_from_file(input_file)
antennas_position = find_antenna(antennas_map)
# Part One
antinodes_part1 = find_antinodes_part1(antennas_position,(len(antennas_map),len(antennas_map[0])))
print("Part One - Number of unique antinode locations:", len(antinodes_part1))
plot_solution(antennas_map, antinodes_part1, antennas_position, "solution_part1.png")
plot_pil(antennas_position, antinodes_part1,(len(antennas_map), len(antennas_map[0])), "solution_part1_pil.png")

# Part Two
antinodes_part2 = find_antinodes_part2(antennas_position,(len(antennas_map),len(antennas_map[0])))
print("Part Two - Number of unique antinode locations:", len(antinodes_part2))
plot_solution(antennas_map, antinodes_part2, antennas_map, "solution_part2.png")
plot_pil(antennas_position, antinodes_part2,(len(antennas_map), len(antennas_map[0])), "solution_part2_pil.png")