import cv2
import numpy as np
from PIL import Image
import math


def get_tictactoe_from_image(image):
    preprocessed_image = preprocess_image(image)

    contours = cv2.findContours(
        preprocessed_image.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[0]

    contour_image = image.copy()
    if contour_image is None:
        print('stoppp!')

    field_image = preprocessed_image.copy()

    # img_contours = np.zeros((100, 100))

    shapes = []
    for contour in contours:
        contour = cv2.approxPolyDP(
            contour, 0.02 * cv2.arcLength(contour, True), True)

        area = cv2.contourArea(contour)
        hull = cv2.convexHull(contour)
        hullArea = cv2.contourArea(hull)

        if hullArea == 0:
            continue
        solidity = area / float(hullArea)

        shape = get_object_shape(solidity, contour)
        # print(shape, solidity)

        middle = cv2.moments(contour)
        if middle["m00"] == 0 or middle["m00"] == 0:
            # print("WARN: zero division error")
            continue

        center_x = middle["m10"] / middle["m00"]
        center_y = middle["m01"] / middle["m00"]

        if shape == "O":
            shapes.append((shape, center_x, center_y))
            # cv2.drawContours(contour_image, [contour], 0, (0, 0, 255), 3)
            cv2.drawContours(field_image, [contour], 0, 0, 3)
        elif shape == "X":
            shapes.append((shape, center_x, center_y))
            # cv2.drawContours(contour_image, [contour], 0, (0, 255, 0), 3)
            cv2.drawContours(field_image, [contour], 0, 0, 3)
        else:
            pass
            # cv2.drawContours(contour_image, [contour], 0, (255, 0, 0), 3)

    resized_image = cv2.resize(field_image,
                               (field_image.shape[0] // 5,
                                field_image.shape[1] // 5))

    edges = cv2.Canny(resized_image, 75, 150)
    lines = cv2.HoughLinesP(edges, 1, np.pi/180, 30,
                            maxLineGap=300,
                            minLineLength=resized_image.shape[0]/2)
    print(lines)
    if lines is None:
        print('stopp2!')
        return None, contour_image

    lines = [line[0] for line in lines]
    new_lines = []

    for line in lines:
        x1, y1, x2, y2 = line
        new_lines.append([x1, y1, x2, y2])
        cv2.line(contour_image, (x1 * 5, y1 * 5),
                                (x2 * 5, y2 * 5), (255, 255, 0), 10)

    board = get_board(new_lines, shapes)

    # image_show(contour_image)  # For testing
    return board, contour_image


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
    threshold = np.bincount(gray_scale_image.flatten()).argmax() * 0.75
    filtered_image = cv2.threshold(
        blurred_image, threshold, 255, cv2.THRESH_BINARY)[1]
    inverted_image = (255-filtered_image)

    return inverted_image


def image_show(im):
    im_pil = Image.fromarray(im)
    im_pil.show()


def get_photo():
    '''
    Get photo from camera stream.
    '''
    image = cv2.imread("./image_processing/assets/4.png")  # For testing
    image = cv2.resize(image, (800, 800))
    return image
