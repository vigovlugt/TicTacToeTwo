import cv2
import numpy as np
from PIL import Image
import time


def get_board_lines(image: np.array, shapes: list,
                    threshold: int = 10, min_line: float = 0.3,
                    max_gap: int = 30) -> list:

    board_image = image.copy()
    # debug_image = np.zeros(image.shape)

    for (shape, _, contour) in shapes:
        if shape in ['X', 'O']:
            cv2.drawContours(board_image, [contour], 0, 0, -1)
    # image_show(board_image)
    # time.sleep(5)

    w, h = image.shape
    edges = cv2.Canny(board_image, 75, 150)
    lines = cv2.HoughLines(edges, 1, np.pi/180, 50)

    if lines is None:
        return None

    lines = [x[0] for x in lines]
    math_lines = []

    for rho, theta in lines:

        x1, y1, x2, y2 = polar_to_euclidian(rho, theta)
        math_lines.append((x1, y1, x2, y2))
        # print(x1, y1, x2, y2)
        # cv2.line(debug_image, (x1, y1), (x2, y2), 120, 2)

    approved = merge_lines(math_lines)
    # print('app:', len(approved), 'all:', len(lines))

    # for x1, y1, x2, y2 in approved:
    #     cv2.line(debug_image, (x1, y1), (x2, y2), np.random.randint(200), 1)
    #     print(x1, y1, x2, y2)

    # image_show(debug_image)
    # time.sleep(3)

    if len(approved) != 4:
        return approved

    return approved


def polar_to_euclidian(rho, theta):

    if np.sin(theta) == 0.0:
        theta = 0.01
    a = rho / np.sin(theta)
    b = -np.cos(theta) / np.sin(theta)

    x1 = 0
    y1 = a
    x2 = 460
    y2 = a + 460 * b

    if y1 > 480:
        y1 = 480
        x1 = (480 - a) / b
    elif y1 < 0:
        y1 = 0
        x1 = -a / b

    if y2 > 480:
        y2 = 480
        x2 = (480 - a) / b
    elif y2 < 0:
        y2 = 0
        x2 = -a / b

    return int(x1), int(y1), int(x2), int(y2)


def dist_point(x1, y1, x2, y2):
    return np.sqrt(pow(x1-x2, 2) + pow(y1-y2, 2))


def merge_lines(lines: list):

    approved = []

    for line in lines:
        same = False
        for i, check_lines in enumerate(approved):
            check_line = check_lines[0]
            if (dist_point(*line[:2], *check_line[:2]) < 40
               and dist_point(*line[2:], *check_line[2:]) < 40):
                same = True
                approved[i].append(line)
                break

            if (dist_point(*line[2:], *check_line[:2]) < 40
               and dist_point(*line[:2], *check_line[2:]) < 40):
                same = True
                approved[i].append(tuple(line[2:] + line[:2]))
                break
        if not same:
            approved.append([line])
    merged = []
    for lines in approved:
        merged.append(calc_average_line(lines))
    # print(len(merged))
    return merged


def calc_average_line(lines):

    def avg(x: list) -> int:
        return int(sum(x) / len(x))

    line = [], [], [], []
    for x1, y1, x2, y2 in lines:
        line[0].append(x1)
        line[1].append(y1)
        line[2].append(x2)
        line[3].append(y2)
    return avg(line[0]), avg(line[1]), avg(line[2]), avg(line[3])


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
        if area < 100:
            continue
        solidity = area / float(hullArea)

        shape = get_object_shape(solidity, contour)

        middle = cv2.moments(contour)
        if middle["m00"] == 0 or middle["m00"] == 0:
            # print("WARN: zero division error")
            continue

        center_x = middle["m10"] / middle["m00"]
        center_y = middle["m01"] / middle["m00"]

        # print(shape, area)
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
