import math


"""
Instead of sorting, try adding to the top right, then bottom left, continuing in advance
Like, for example on a list of values 1-16, add in this order:
16,15,13,10
14,12,09,06
11,08,05,03
07,04,02,01
The order *along each diagonal* may change

Order for a 4x4, split by diagonal:
(0,0)
(1,0), (0,1),
(2,0), (1,1), (0,2)
(3,0), (1,2), (2,1), (0,3)
(3,1), (2,2), (1,3)
(3,2), (2,3)
(3,3)

Number of diagonals for each side length:
1: 1
2: 3
3: 5
4: 7
5: 9
Formula: s*2-1
"""


def to_grid_diagonal(input: list[int]) -> list[list[int]]:
    num_stack = input.copy()
    num_stack.sort(reverse=True)
    side = math.isqrt(len(input))
    grid = [list(range(side)) for _ in range(side)] # Initialize 2d array

    for x0 in range(side*2-1): # Iterate number of diagonals
        x = min(x0, side-1)
        y = max(0, x0-side+1)
        while y <= min(x0, side-1):
            n = num_stack.pop(0)
            # print(x, y )
            grid[x][y] = n
            x -= 1
            y += 1


    return grid


def is_grid_sorted(input: list[list[int]]) -> bool:
    # Row-wise sorted?
    for row in input:
        s = row[0]
        for n in row[1:]:
            if n >= s:
                return False
            s = n

    # Column-wise sorted?
    for i in range(len(input[0])):
        s = input[i][0]
        for j in range(1, len(input)):
            n = input[j][i]
            if n >= s:
                return False
            s = n

    return True


def print_grid(input: list[list[int]]):
    for row in input:
        print(row)

def evaluate():
    with open("RandomNumbers.txt") as f:
        numbers: list[list[int]] = [eval(line) for line in f.readlines()]

    fails = 0
    for input in numbers:
        grid = to_grid_diagonal(input)
        if is_grid_sorted(grid):
            print("SUCCESS")
            print_grid(grid)
        else:
            print("FAIL")
            print(input)
            fails += 1

    print(fails, "total fails")

evaluate()
