import cv2


def get_line_orientation(line):
    x1, y1, x2, y2 = line

    if (x2-x1) == 0:
        return "VERTICAL"

    a = (y2-y1)/(x2-x1)
    if a > 1 or a < -1:
        return "VERTICAL"
    return "HORIZONTAL"


def get_line_average_x(line):
    x1, y1, x2, y2 = line
    return (x1 + x2) / 2


def get_line_average_y(line):
    x1, y1, x2, y2 = line
    return (y1 + y2) / 2


def get_relative_position(num, nums):
    if num < nums[0]:
        return 2
    elif num > nums[0] and num < nums[1]:
        return 1
    elif num > nums[1]:
        return 0


def get_board(lines, shapes):
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
        # print(board_x, board_y)
        board[board_y][board_x] = shape

    return board
