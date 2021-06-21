import cv2
import numpy as np
from PIL import Image
import math


def get_tictactoe_from_image(preprocessed_image):
    image = preprocessed_image

    contours = cv2.findContours(
        preprocessed_image.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[0]

    contour_image = image.copy()

    img_contours = np.zeros(image.shape[0:2])

    shapes = []
    for contour in contours:
        approx = cv2.approxPolyDP(
            contour, 0.02 * cv2.arcLength(contour, True), True)

        contour = approx

        area = cv2.contourArea(contour)
        hull = cv2.convexHull(contour)
        hullArea = cv2.contourArea(hull)

        if hullArea == 0:
            continue
        solidity = area / float(hullArea)

        shape = get_object_shape(solidity, approx)
        # print(shape, solidity)

        middle = cv2.moments(contour)
        if middle["m00"] == 0 or middle["m00"] == 0:
            # print("WARN: zero division error")
            continue

        center_x = middle["m10"] / middle["m00"]
        center_y = middle["m01"] / middle["m00"]

        if shape == "O":
            shapes.append((shape, center_x, center_y))
            cv2.drawContours(contour_image, [contour], 0, (0, 0, 255), 3)
        elif shape == "X":
            shapes.append((shape, center_x, center_y))
            cv2.drawContours(contour_image, [contour], 0, (0, 255, 0), 3)
        else:
            cv2.drawContours(contour_image, [contour], 0, (255, 0, 0), 3)
            cv2.drawContours(img_contours, [contour], 0, 255, 30)

    img_contours = np.uint8(img_contours)
    img_contours = cv2.resize(img_contours, (100, 100))

    edges = cv2.Canny(img_contours, 75, 150)
    lines = cv2.HoughLinesP(edges, 1, np.pi/180, 30,
                            maxLineGap=300, minLineLength=80)

    if lines is None:
        return None

    lines = [line[0] for line in lines]
    new_lines = []

    for line in lines:
        x1, y1, x2, y2 = line
        x1, y1, x2, y2 = 8*x1, 8*y1, 8*x2, 8*y2
        new_lines.append([x1, y1, x2, y2])
        cv2.line(contour_image, (x1, y1), (x2, y2), (255, 255, 0), 10)

    board = get_board(new_lines, shapes)

    # image_show(contour_image)  # For testing
    return board


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

    for shape, x, y in shapes:
        board_y = get_relative_position(y, line_ys)
        board_x = 2 - get_relative_position(x, line_xs)
        board[board_y][board_x] = shape

    return board


def print_board(board):
    for y in range(3):
        for x in range(3):
            if board[y][x] is not None:
                print(board[y][x], end="")
            else:
                print(" ", end="")
        print()


def get_object_shape(solidity, approx):
    if len(approx) == 4:
        return "RECTANGLE"
    elif len(approx) > 15:
        return "POLYGON"
    elif solidity > 0.9:
        return "O"
    elif solidity > 0:
        return "X"


def preprocess_image(image):
    gray_scale_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred_image = cv2.GaussianBlur(gray_scale_image, (5, 5), 0)
    filtered_image = cv2.threshold(
        blurred_image, 128, 255, cv2.THRESH_BINARY)[1]
    inverted_image = (255-filtered_image)

    return inverted_image


def image_show(im):
    im_pil = Image.fromarray(im)
    im_pil.show()


# class Line:
#     start: tuple
#     end: tuple

#     def __init__(x1, y1, x2, y2):
#         if y1 > y2:
#             start = (x2, y2)
#             end = (x1, y1)
#         else:
#             start = (x1, y1)
#             end = (x2, y2)


def same_line(line1, line2):
    (x11, y11, x21, y21) = line1
    rc_line1 = abs(y11 - y21) / abs(x11 - x21)

    (x12, y12, x22, y22) = line2
    rc_line2 = abs(y12 - y22) / abs(x12 - x22)

    print(rc_line1, rc_line2, math.degrees(np.arctan(rc_line1)),
          math.degrees(np.arctan(rc_line2)))


def line_length(x1, y1, x2, y2):
    return np.sqrt(pow(x1 - x2, 2) + pow(y1 - y2, 2))


def merge_lines(lines):

    confirmed_lines = []

    for line in lines:
        same_line(line, lines[0])
    return lines


def get_photo():
    '''
    Get photo from camera stream.
    '''
    image = cv2.imread("./image_processing/assets/4.png")  # For testing
    image = cv2.resize(image, (800, 800))
    return image
