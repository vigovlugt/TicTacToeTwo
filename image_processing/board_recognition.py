'''
Names: J. Boon, F. Hoetjes, J. Siegers, V. Vlugt & L. van der Waals
MM_Group: 3
Study: BSc Informatica
board_recognition.py:
    - This program detects the lines which make up the board.
    - It also detects all shapes (circles and crosses) on the board.
    - It then returns a 2-dimensional array with O, X or None in the cells
      which represents the board.
'''


def get_line_orientation(line):
    '''
    Gets line orientation, returns "VERTICAL" or "HORIZONTAL".
    '''
    x1, y1, x2, y2 = line

    if (x2-x1) == 0:
        return "VERTICAL"

    a = (y2-y1)/(x2-x1)
    if a > 1 or a < -1:
        return "VERTICAL"
    return "HORIZONTAL"


def get_line_average_x(line):
    '''
    Gets the average of line x, returns one line.
    '''
    x1, y1, x2, y2 = line
    return (x1 + x2) / 2


def get_line_average_y(line):
    '''
    Gets the average of line y, returns one line.
    '''
    x1, y1, x2, y2 = line
    return (y1 + y2) / 2


def get_relative_position(num, nums):
    '''
    Gets relative position between two lines.
    '''
    if num < nums[0]:
        return 2
    elif num > nums[0] and num < nums[1]:
        return 1
    elif num > nums[1]:
        return 0


def get_board(lines, shapes):
    '''
    Gets the board and all of its values, returns the board.
    '''
    board = [[None, None, None], [None, None, None], [None, None, None]]

    vertical_lines = [
        line for line in lines if get_line_orientation(line) == "VERTICAL"]
    horizontal_lines = [
        line for line in lines if get_line_orientation(line) == "HORIZONTAL"]

    if len(vertical_lines) != 2 or len(horizontal_lines) != 2:
        return None

    line_ys = sorted([get_line_average_y(line) for line in horizontal_lines])
    line_xs = sorted([get_line_average_x(line) for line in vertical_lines])

    for shape, (x, y), _ in shapes:
        if shape != "O" and shape != "X":
            continue

        board_y = get_relative_position(y, line_ys)
        board_x = 2 - get_relative_position(x, line_xs)
        board[board_y][board_x] = shape

    return board
