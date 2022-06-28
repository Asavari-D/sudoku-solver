# grid = [
#     [7,8,0,4,0,0,1,2,0],
#     [6,0,0,0,7,5,0,0,9],
#     [0,0,0,6,0,1,0,7,8],
#     [0,0,7,0,4,0,2,6,0],
#     [0,0,1,0,5,0,9,3,0],
#     [9,0,4,0,6,0,0,0,5],
#     [0,7,0,3,0,0,0,1,2],
#     [1,2,0,0,0,7,4,0,0],
#     [0,4,9,2,0,6,0,0,7]
# ]

def solve(grid, row, col, num):
    for i in range(9):
        if grid[row][i] == num:
            return False
    for j in range(9):
        if grid[i][col] == num:
            return False

    start_row = row - row%3
    start_col = col - col%3
    for i in range(3):
        for j in range(3):
            if grid[i + start_row][j + start_col] == num:
                return False

    return True

def sudoku(grid, row, col):
    if (row==8 and col==9):
        return True

    if col==9:
        row+=1
        col=0

    if grid[row][col] > 0:
        return sudoku(grid, row, col+1)

    for num in range(1, 10):
        if solve(grid, row, col, num):
            grid[row][col] = num
            if sudoku(grid, row, col+1):
                return True
        grid[row][col] = 0
    return False




