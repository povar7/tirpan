BOARD_SIZE = 0

def under_attack(col, queens):
    left = right = col
    for r, c in reversed(queens):
        left, right = left - 1, right + 1
        if c in (left, col, right):
            return True
    return False

def solve2(n):
    if n == 0: return [[]] # No RECURSION if n=0. 
    smaller_solutions = solve2(n - 1) # RECURSION!!!!!!!!!!!!!!
    solutions = []
    for solution in smaller_solutions: # I moved this around, so it makes more sense
        for column in range(1, BOARD_SIZE + 1): # I changed this, so it makes more sense
            # try adding a new queen to row = n, column = column 
            if not under_attack(column, solution): 
                solutions.append(solution + [(n, column)])
    return solutions

def solve(n):
    if not isinstance(n, (int, long)) or n < 0:
        return []
    else:
        return solve2(n) 

for answer in solve(BOARD_SIZE):
    print answer

