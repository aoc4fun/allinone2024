def read_input(filename):
    with open(filename, 'r') as file:
        return file.readline().strip()

def main():
    line = read_input('09.txt')
    # Create memory as list of tuples (count, value)
    memory = []
    for i, x in enumerate(line):
        memory.append((int(x), int(i/2) if i%2==0 else "."))
    
    # Process blocks from end to start
    for i in range(len(memory)-1, -1, -1):
        dots_needed, value = memory[i]
        if value != ".":
            # Find a spot from the beginning where this block would fit
            current_pos = 0
            while (current_pos < i and 
                    (memory[current_pos][1] != "." or
                    memory[current_pos][0] < dots_needed)):
                current_pos += 1
            
            if current_pos < i:  # Found enough space
                # Move the block
                new_memory = memory[:current_pos] + [(dots_needed, value)]
                if(memory[current_pos][0] - dots_needed > 0):
                    new_memory += [(memory[current_pos][0] - dots_needed, ".")]
                new_memory += memory[current_pos+1:i] + [(dots_needed, ".")] + memory[i+1:]
                memory = new_memory
            

    
    
    # Calculate sum of products (number * index)
    total = 0
    current_index = 0
    for count, value in memory:
        if value != ".":
            # Add product for each position in the block
            for i in range(count):
                total += value * (current_index + i)
        current_index += count
    
    print(f"Sum of products (number * index): {total}")

if __name__ == "__main__":
    main()
