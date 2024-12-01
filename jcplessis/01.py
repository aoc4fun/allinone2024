def load_data():
    with open('01.txt', 'r') as file:
        lines = file.readlines()
    
    first_parts = []
    second_parts = []
    
    for line in lines:
        # Split on three spaces and strip any whitespace
        parts = line.strip().split('   ')
        first_parts.append(parts[0])
        second_parts.append(parts[1])
    
    return first_parts, second_parts

# Example usage
first_list, second_list = load_data()

# Sort both lists
first_list.sort()
second_list.sort()

# Create pairs and compute distances
pairs = list(zip(first_list, second_list))
distances = []

for first, second in pairs:
    # Convert strings to integers and compute absolute difference
    distance = abs(int(first) - int(second))
    distances.append(distance)

print("Pairs:", pairs)
print("Distances:", distances)
print("Sum of all distances:", sum(distances))

# Create frequency pairs and compute products
frequency_pairs = []
products = []
for element in first_list:
    count = second_list.count(element)
    frequency_pairs.append((element, count))
    # Convert element to int and multiply by its frequency
    product = int(element) * count
    products.append(product)

print("Frequency pairs:", frequency_pairs)
print("Products (element * frequency):", products)
print("Sum of all products:", sum(products))
