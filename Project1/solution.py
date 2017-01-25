assignments = []
rows = 'ABCDEFGHI'
cols = '123456789'
diag1 = [['A1','B2','C3','D4','E5','F6','G7','H8','I9']]
diag2 = [['A9','B8','C7','D6','E5','F4','G3','H2','I1']]


def cross(a, b):
    return [s+t for s in a for t in b]

boxes = cross(rows, cols)
row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
unitlist = row_units + column_units + square_units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """

    # Find all instances of naked twins
    # Eliminate the naked twins as possibilities for their peers
    twins1 = []
    twins2 = []
    size_2 = [i for i in values.keys() if len(values[i])==2]
    for i in size_2:
        for peer in peers[i]:
            if values[peer]==values[i]:
                twins1.append(i)
                twins2.append(peer)
    for first_twin,second_twin in zip(twins1,twins2):
        for unit in unitlist:
            if first_twin in unit and second_twin in unit:
                for box in unit:
                    if box!=first_twin and box!=second_twin:
                        for digit in values[first_twin]:
                            values[box] = values[box].replace(digit,'')

    return values

                            
        


def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    # pass
    sudoku = []
    digits = '123456789'
    for c in grid:
        if c in digits:
            sudoku.append(c)
        if c == '.':
            sudoku.append(digits)
    assert len(sudoku) == 81
    return dict(zip(boxes, sudoku))


def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    # pass
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return

def eliminate(values):
    # pass
    single_constraint = [i for i in values.keys() if len(values[i])==1]
    for i in single_constraint:
        val = values[i]
        for peer in peers[i]:
            values[peer] = values[peer].replace(val,'')
            # assign_value(values,peer,'')
    return values

def only_choice(values):
    # pass
    for unit in unitlist:
        for digit in '123456789':
            possible_digit_places = []
            for box in unit:
                if(digit in values[box]):
                    possible_digit_places.append(box)
            if(len(possible_digit_places)==1):
                # values[possible_digit_places[0]] = digit
                assign_value(values,possible_digit_places[0],digit)
    return values

def reduce_puzzle(values):
    # pass
    stop = False
    while not stop:
        
        solved_uptil_now = 0
        for box in values.keys():
            solved_uptil_now = solved_uptil_now + len(values[box])
        values = eliminate(values)
        values = only_choice(values)
        values = naked_twins(values)
        solved_after_stratergy = 0
        for box in values.keys():
            solved_after_stratergy = solved_after_stratergy + len(values[box])
        if(solved_after_stratergy ==  solved_uptil_now):
            stop = True      
    return values

def search(values):
    # pass
    values = reduce_puzzle(values)
    if values == False:
        return False
    solved = 0
    for box in values.keys():
        if(len(values[box])==1):
            solved+=1
    if(solved == 81):
        return values
    mini = 10
    mini_box = 'A1'
    for box in values.keys():
        if(len(values[box])<mini and len(values[box])!=1):
            mini = len(values[box])
            mini_box = box
    poss_digits = values[mini_box]
    for digit in poss_digits:
        temp_sudoku = values.copy()
        temp_sudoku[mini_box] = digit
        complete = search(temp_sudoku)
        if complete:
            return complete

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The string representing the final sudoku grid. False if no solution exists.
    """
    str_to_values = grid_values(grid)
    global unitlist
    unitlist = unitlist+diag2+diag1
    ans = search(str_to_values)
    if ans == False:
        return False
    return ans
    # values_to_str = ""
    # for i in values.keys()


if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
