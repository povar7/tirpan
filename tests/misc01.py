print 'Hello, world!'

name = raw_input('What is your name?\n')
print 'Hi, %s.' % name

friends = ['john', 'pat', 'gary', 'michael']
for i, name in enumerate(friends):
    print 'iteration {iteration} is {name}'.format(iteration=i, name=name)

parents, babies = (1, 1)
while babies < 100:
    print 'This generation has {0} babies'.format(babies)
    parents, babies = (babies, parents + babies)

def greet(name):
    print 'Hello', name
greet('Jack')
greet('Jill')
greet('Bob')

import re
for test_string in ['555-1212', 'ILL-EGAL']:
    if re.match(r'^\d{3}-\d{4}$', test_string):
        print test_string, 'is a valid US local phone number'
    else:
        print test_string, 'rejected'

prices = {'apple': 0.40, 'banana': 0.50}
my_purchase = {
    'apple': 1,
    'banana': 6}
grocery_bill = sum(prices[fruit] * my_purchase[fruit]
                   for fruit in my_purchase)
print 'I owe the grocer $%.2f' % grocery_bill

import sys
try:
    total = sum(int(arg) for arg in sys.argv[1:])
    print 'sum =', total
except ValueError:
    print 'Please supply integer arguments'

# indent your Python code to put into an email
import glob
# glob supports Unix style pathname extensions
python_files = glob.glob('*.py')
for file_name in sorted(python_files):
    print '    ------' + file_name
    with open(file_name) as f:
        for line in f:
            print '    ' + line.rstrip()
    print

from time import localtime

activities = {8: 'Sleeping',
              9: 'Commuting',
              17: 'Working',
              18: 'Commuting',
              20: 'Eating',
              22: 'Resting' }

time_now = localtime()
hour = time_now.tm_hour

for activity_time in sorted(activities.keys()):
    if hour < activity_time:
        print activities[activity_time]
        break
else:
    print 'Unknown, AFK or sleeping!'

REFRAIN = '''
%d bottles of beer on the wall,
%d bottles of beer,
take one down, pass it around,
%d bottles of beer on the wall!
'''
bottles_of_beer = 99
while bottles_of_beer > 1:
    print REFRAIN % (bottles_of_beer, bottles_of_beer,
        bottles_of_beer - 1)
    bottles_of_beer -= 1

def median(pool):
    '''Statistical median to demonstrate doctest.
    >>> median([2, 9, 9, 7, 9, 2, 4, 5, 8])
    7
    '''
    copy = sorted(pool)
    size = len(copy)
    if size % 2 == 1:
        return copy[(size - 1) / 2]
    else:
        return (copy[size / 2 - 1] + copy[size / 2]) / 2

median([2, 9, 9, 7, 9, 2, 4, 5, 8])

BOARD_SIZE = 8

def under_attack(col, queens):
    left = right = col
    for r, c in reversed(queens):
        left, right = left - 1, right + 1
        if c in (left, col, right):
            return True
    return False

def solve(n):
    if n == 0: return [[]] # No RECURSION if n=0. 
    smaller_solutions = solve(n - 1) # RECURSION!!!!!!!!!!!!!!
    solutions = []
    for solution in smaller_solutions: # I moved this around, so it makes more sense
        for column in range(1, BOARD_SIZE + 1): # I changed this, so it makes more sense
            # try adding a new queen to row = n, column = column 
            if not under_attack(column, solution): 
                solutions.append(solution + [(n, column)])
    return solutions

for answer in solve(BOARD_SIZE):
    print '==='
    for x, y in answer:
        print x, y
