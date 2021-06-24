'''
Names: J. Boon, F. Hoetjes, J. Siegers, V. Vlugt & L. van der Waals
MM_Group: 3
Study: BSc Informatica
affine_transformation.py:
    - This program uses an affine transformation to get the correct perspective
      of the shapes that will be drawn on the visual playing field.
    - It also draws these shapes on the visual playing field accordingly.
    - If a player removes his move from the board, this program will make sure
      it is still visible on the visual playing field.
'''

import cv2
import numpy as np
from PIL import Image
from shapely.geometry import LineString
from shapely.geometry import Point


def get_affine_transform(lines, image, board, detected_board):
    '''
    This method returns an image with all shapes not present on the
    physical paper in the image. If the image is rotated or not straight,
    this method transforms the projected shapes to that rotation and then
    draws the shape on the image.
    '''

    points = []
    lines = [[tuple(line[:2]), tuple(line[2:])] for line in lines]

    for line in lines:
        for check_line in lines:
            intersect = LineString(line).intersection(LineString(check_line))
            if isinstance(intersect, Point) and intersect not in points:
                points.append(intersect)

    std_points = [[p.x, p.y] for p in points]
    std_points = sorted(std_points, key=lambda x: x[0])
    tl = min(std_points[:2], key=lambda x: x[1])
    tr = max(std_points[:2], key=lambda x: x[1])
    bl = min(std_points[2:], key=lambda x: x[1])
    br = max(std_points[2:], key=lambda x: x[1])

    std_points = np.array([tl, tr, bl, br], np.float32)

    dest_points = np.array([[30, 30], [30, 60], [60, 30],
                            [60, 60]], np.float32)

    projective_matrix = cv2.getPerspectiveTransform(dest_points, std_points)

    shapes = get_ai_shapes_on_board(board, detected_board)

    for shape, poly in shapes:
        nc = cv2.perspectiveTransform(poly, projective_matrix)[0]

        if shape == 'X':
            cv2.line(image, tuple(nc[0]), tuple(nc[1]), (32, 32, 32), 3)
            cv2.line(image, tuple(nc[2]), tuple(nc[3]), (32, 32, 32), 3)
        elif shape == 'O':
            cv2.polylines(image, [nc.astype(np.int32)], True, (32, 32, 32), 3)

    return image


def image_show(im):
    '''
    Helper function which shows the image on the screen.
    Useful for debugging.
    '''
    im_pil = Image.fromarray(im)
    im_pil.show()


def get_ai_shapes_on_board(board, detected_board):
    '''
    Returns an array of circles and crosses which exists in
    the digital board but not on the physical board.
    If the computer has put a O in cell 1-1, this O is represented
    as a polygon with the correct coordinates in the array this method returns.
    '''
    shapes = []

    for y in range(3):
        for x in range(3):
            shape = board[x][y]
            detected_shape = detected_board[x][y]

            if detected_shape == shape:
                continue

            if shape == "O":
                poly = get_circle()
            elif shape == "X":
                poly = get_cross()
            else:
                continue

            offset_x = 60 - x * 30
            offset_y = y * 30

            for i in range(len(poly[0])):
                poly[0][i][0] += offset_y
                poly[0][i][1] += offset_x

            shapes.append((shape, poly))

    return shapes


def get_cross():
    '''
    Get an array with the two lines which represent a cross.
    '''
    return np.array([[[10, 10], [20, 20], [10, 20], [20, 10]]], np.float32)


def get_circle():
    '''
    Get a polygon of a circle with radius 7.5 at position 15, 15
    '''
    p = Point(15, 15)
    circle = p.buffer(7.5)
    return np.array([circle.exterior.coords])
