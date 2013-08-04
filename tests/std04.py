BOARD_SIZE = 8

def under_attack(col, queens):
    left = right = col
    for r, c in reversed(queens):
        left, right = left - 1, right + 1
        if c in (left, col, right):
            return True
    return False

def solve2(n):
    if n == 0:
        return [[]]

    smaller_solutions = solve2(n - 1)
    solutions = []

    for solution in smaller_solutions:
        for column in range(1, BOARD_SIZE + 1):
            if not under_attack(column, solution):
                solutions.append(solution + [(n, column)])

    return solutions

def solve(n):
    if not isinstance(n, (int, long)) or n < 0:
        return []
    else:
        return solve2(n)

def print_results():
    global x, y
    for answer in solve(BOARD_SIZE):
       print '==='
       for x1, y1 in answer:
           print x1, y1
           x = x1
           y = y1

print_results()
print
print x
print y
