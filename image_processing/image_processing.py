import cv2
import numpy as np
from PIL import Image
import math
import time


def get_board_lines(image: np.array, shapes: list,
                    resize_factor: int = 1, threshold: int = 10,
                    min_line: float = 0.3, max_gap: int = 30) -> list:
    board_image = image.copy()

    debug_image = np.zeros(image.shape)

    for (shape, _, contour) in shapes:
        if shape in ['X', 'O']:
            cv2.drawContours(board_image, [contour], 0, 0, -1)

    rf = resize_factor
    w, h = image.shape
    resized_image = board_image # cv2.resize(board_image, (w // rf, h // rf))
    edges = cv2.Canny(resized_image, 75, 150)
    lines = cv2.HoughLines(edges, 1, np.pi/180, 80)
    print(threshold, max_gap, w * min_line)
    print(lines)

    # lines = [(x1 * rf, y1 * rf, x2 * rf, y2 * rf) for [(x1, y1, x2, y2)] in lines]
    # for line in lines:
    #     cv2.line(debug_image, line[:2], line[2:], np.random.randint(255), 10)

    # lines = [x[0] for x in lines]
    # if lines is not None:
    #     for i in range(0, len(lines)):
    #         print('x')
    #         rho = lines[i][0][0]
    #         theta = lines[i][0][1]
    #         a = np.cos(theta)
    #         b = np.sin(theta)
    #         x0 = a*rho
    #         y0 = b*rho
    #         x1 = int(x0 + 1000*(-b))
    #         y1 = int(y0 + 1000*(a))
    #         x2 = int(x0 - 1000*(-b))
    #         y2 = int(y0 - 1000*(a))


    lines = [x[0] for x in lines]
    approved = merge_lines(lines)
    print('app:', len(approved), 'all:', len(lines))
    # draw lines
    for rho, theta in approved:

        
        # a = np.cos(theta)
        # b = np.sin(theta)
        # x0 = a*rho
        # y0 = b*rho
        # x1 = int(x0 + 1000*(-b))
        # y1 = int(y0 + 1000*(a))
        # x2 = int(x0 - 1000*(-b))
        # y2 = int(y0 - 1000*(a))
        cv2.line(debug_image, (x1, y1), (x2, y2), 255, 2)
        print((x1, y1), (x2, y2))
    image_show(debug_image)
    time.sleep(5)

    if len(lines) != 4:
        return None

    return [(x1 * rf, y1 * rf, x2 * rf, y2 * rf) for (x1, y1, x2, y2) in lines]


def merge_lines(lines: list):

    approved = []

    for line in lines:
        same = False
        for i, check_line in enumerate(approved):
            if (abs(check_line[0] - line[0]) < 30
               and abs(check_line[1] - line[1]) < 0.15):
                same = True
                break
        if not same:
            approved.append(line)
    return approved


def image_show(im):
    im_pil = Image.fromarray(im)
    im_pil.show()


def get_shapes(image):
    shapes = []

    contours = cv2.findContours(
        image.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[0]

    for contour in contours:


        area = cv2.contourArea(contour)
        hull = cv2.convexHull(contour)
        hullArea = cv2.contourArea(hull)

        if hullArea == 0:
            continue
        solidity = area / float(hullArea)

        shape = get_object_shape(solidity, contour)

        middle = cv2.moments(contour)
        if middle["m00"] == 0 or middle["m00"] == 0:
            # print("WARN: zero division error")
            continue

        center_x = middle["m10"] / middle["m00"]
        center_y = middle["m01"] / middle["m00"]

        shapes.append((shape, (center_x, center_y), contour))

    return shapes


def get_object_shape(solidity, contour, simplify=0.02):
    approx = cv2.approxPolyDP(
            contour, simplify * cv2.arcLength(contour, True), True)
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
    threshold = np.bincount(gray_scale_image.flatten()).argmax() * 0.5
    filtered_image = cv2.threshold(
        blurred_image, threshold, 255, cv2.THRESH_BINARY)[1]
    inverted_image = (255-filtered_image)

    return inverted_image
