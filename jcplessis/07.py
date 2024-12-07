def parse_line(line):
    """Parse a line into target number and list of operands."""
    target, numbers = line.strip().split(':')
    return int(target), [int(x) for x in numbers.split()]

def evaluate_left_to_right(numbers, operators):
    """Evaluate expression from left to right."""
    if len(numbers) != len(operators) + 1:
        raise ValueError("Invalid number of operators")
    
    result = numbers[0]  # Start with leftmost number
    
    # Process operators left to right
    for i in range(len(operators)):
        if operators[i] == '+':
            result = result + numbers[i + 1]
        elif operators[i] == '*':
            result = result * numbers[i + 1]
        else:  # '|' concatenation
            result = int(str(result) + str(numbers[i + 1]))
            
    return result

def find_operators(target, numbers):
    """Find operators that produce the target when evaluated left to right."""
    operators = ['+', '*', '|']  # Added '|' operator
    n = len(numbers) - 1  # Number of operators needed
    
    # Try all possible combinations of operators
    for i in range(3 ** n):  # 3^n possible combinations (now 3 operators)
        current_ops = []
        temp = i
        for _ in range(n):
            current_ops.append(operators[temp % 3])
            temp //= 3
                
        result = evaluate_left_to_right(numbers, current_ops)
        if result == target:
            return current_ops
    
    return None

def solve_file(filename):
    total = 0  # Initialize sum
    with open(filename, 'r') as file:
        for line in file:
            target, numbers = parse_line(line)
            operators = find_operators(target, numbers)
            if operators:  # If solution exists
                total += target  # Add target to sum
                # Create expression string for display
                expr = ''
                for i in range(len(numbers)):
                    expr += str(numbers[i])
                    if i < len(operators):
                        expr += operators[i]
                print(f"{expr} = {target}")
            else:
                print(f"No solution found for target {target} with numbers {numbers}")
    
    print(f"\nSum of solvable target numbers: {total}")  # Print final sum
    return total  # Return the sum

# Run the solver
sum_result = solve_file('07.txt')
