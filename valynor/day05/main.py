sample="""47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47"""

with open("05.txt","r") as f:
    input_data=f.read()

def parse_data(input_data):
    rules, order_print=input_data.split("\n\n")
    return [list(map(int, line.split("|"))) for line in rules.split("\n")], [list(map(int, line.split(","))) for line in order_print.split("\n")]
#lines = [line.strip() for line in sys.stdin if line.strip()]
#for line in lines:
#    if '|' in line:
#        ordering_rules.append(list(map(int,line.split("|"))))
#    elif ',' in line:
#        updates.append(list(map(int,line.split(","))))

def is_correct(rules, update):
    for X, Y in rules:
        if X in update and Y in update:
            if update.index(X) >= update.index(Y):
                return False
    return True

def find_ordered_unordered(rules, order_print):
    correct_updates = []
    incorrect_updates = []
    for update in order_print:
        if is_correct(rules, update):
            correct_updates.append(update)
        else:
            incorrect_updates.append(update)
    return correct_updates,incorrect_updates

def correct_unordering(rules, unordered_order_print):
    corrected_updates = []
    for pages in unordered_order_print:
        while is_correct(rules, pages) == False:
          for X, Y in rules:
            if X in pages and Y in pages:
                if pages.index(X) >= pages.index(Y):
                    pages[pages.index(X)],pages[pages.index(Y)]=pages[pages.index(Y)],pages[pages.index(X)]
        corrected_updates.append(pages)
    return corrected_updates

compute_middle=lambda a:sum([pages[len(pages)//2] for pages in a])

rules_sample, order_print_sample=parse_data(sample)
ordered_sample, unordered_sample = find_ordered_unordered(*parse_data(sample))
rules, order_print=parse_data(input_data)
ordered, unordered = find_ordered_unordered(*parse_data(input_data))

#print(compute_middle(find_correct_list(find_predecessors(parse_data(sample)[0]),parse_data(sample)[1])))
assert(compute_middle(ordered_sample)==143)
print(f"Part 1 result : {compute_middle(ordered)}")

assert(compute_middle(correct_unordering(rules_sample,unordered_sample))==123)
print(f"Part 2 result : {compute_middle(correct_unordering(rules,unordered))}")