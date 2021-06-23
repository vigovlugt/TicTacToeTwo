import cv2
import numpy as np
from PIL import Image
import math
import time
import matplotlib.pyplot as plt
from shapely.geometry import LineString
from shapely.geometry import Point


def get_affine_transform(lines, image, board):

    # if lines != 4:
    #     for line in lines:
    #         cv2.line(image, tuple(line[2:]), tuple(line[:2]), (120, 0, 255), 3)
    #     return image
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
    # print(image.shape)
    # dest_points = np.array([[160, 153], [160, 306], [320, 153], [320, 306]], np.float32)
    # dest_points = np.array([[160, 153], [160, 153], [320, 306], [320, 306]], np.float32)
    dest_points = np.array([[30, 30], [30, 60], [60, 30], [60, 60]], np.float32)

    # print(std_points, dest_points)
    projective_matrix = cv2.getPerspectiveTransform(dest_points, std_points)

    test_cross = np.array([[[5, 5], [25, 25], [5, 25], [25, 5]]], np.float32)

    im = cv2.warpPerspective(image, projective_matrix, (480, 460))

    crosses = get_ai_crosses_on_board(board)

    for cross in crosses:
        nc = cv2.perspectiveTransform(cross, projective_matrix)[0]
        cv2.line(image, tuple(nc[0]), tuple(nc[1]), (255, 0, 0), 3)
        cv2.line(image, tuple(nc[2]), tuple(nc[3]), (255, 0, 0), 3)
    # image_show(im)
    # time.sleep(10)
    return image


def image_show(im):
    im_pil = Image.fromarray(im)
    im_pil.show()


def get_ai_crosses_on_board(board):
    crosses = []
    base_cross = np.array([[[5, 5], [25, 25], [5, 25], [25, 5]]], np.float32)

    for y in range(3):
        for x in range(3):
            # print(board)
            shape = board[x][y]
            if shape != "O":
                continue

            offset_x = 60 - x * 30
            offset_y = y * 30

            new_cross = base_cross.copy()
            for i in range(4):
                new_cross[0][i][0] += offset_y
                new_cross[0][i][1] += offset_x

            crosses.append(new_cross)

    return crosses
