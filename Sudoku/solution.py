assignments = []

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """

    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values

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
    # Find all instances of naked twins
    
    twins = [box for box in values.keys() if len(values[box]) == 2]
    naked_twins = [[boxA, boxB] for boxA in twins for boxB in peers[boxA] if set(values[boxA]) == set(values[boxB])]
    
    # Eliminate the naked twins as possibilities for their peers
    
    for pair in naked_twins:
        twins_peer = [box for box in peers[pair[0]] if box in peers[pair[1]]]
        for box in twins_peer:
            for d in values[pair[0]]:
                values = assign_value(values, box, values[box].replace(d,''))
    return values            

def cross(A, B):
    """
    Cross product of elements in A and elements in B.
    """
    return [s+t for s in A for t in B]

rows = 'ABCDEFGHI'
cols = '123456789'

boxes = cross(rows, cols)

row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
diag_units = [[rows[i]+cols[i] for i in range(len(rows))]] + [[rows[i]+cols[8-i] for i in range(len(rows))]]
diag_sudoku = 0 # set this equals to 1 for normal sudoku
if diag_sudoku == 0:
    unitlist = row_units + column_units + square_units+diag_units
else:
    initlist = row_units + column_units + square_units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)



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
    values = []
    digits = '123456789'
    for c in grid:
        if c in digits:
            values.append(c)
        if c == '.':
            values.append(digits)
    assert len(values) == 81
    return dict(zip(boxes, values))


def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return

def eliminate(values):
    
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        d = values[box]
        for peer in peers[box]:
            # eliminate d from peers
            value = values[peer].replace(d,'')
            values = assign_value(values, peer, value)
    return values

def only_choice(values):
    for unit in unitlist:
        for digit in '123456789':
            place = [box for box in unit if digit in values[box]]
            if len(place) == 1:
                # values[place[0]] = digit
                values = assign_value(values, place[0], digit)
    return values

def reduce_puzzle(values):
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

        # Use the Eliminate Strategy
        eliminate(values)
        # Use the Only Choice Strategy
        only_choice(values)
        # Use Naked Twins Strategy
        naked_twins(values)
        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values


def search(values):
    """
    Using depth-first search and propagation, create a search tree and solve the sudoku.
    """
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)
    if values == False:
        return False
    if all(len(values[box]) == 1 for box in values.keys()):
        return values # the sodoku is solved!
    
    # Choose one of the unfilled squares with the fewest possibilities
    n,s = min((len(values[s]),s) for s in boxes if len(values[s]) > 1)
    # Now use recursion to solve each one of the resulting sudokus, and if one returns a value (not False), return that answer!
    for digit in values[s]:
        new = values.copy()
        new[s] = digit
        attempt = search(new)
        if attempt:
            return attempt

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    values = grid_values(grid)
    values = search(values)
        
    return values

if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
