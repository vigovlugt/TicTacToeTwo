import cv2
import numpy as np


def get_tictactoe_from_image(image):
    preprocessed_image = preprocess_image(image)

    contours = cv2.findContours(
        preprocessed_image.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[0]

    contour_image = image.copy()
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

        shape = get_object_shape(solidity)
        print(shape, solidity)

        is_rectangle = len(approx) == 4
        is_grid = len(approx) > 15

        if shape == "O" and not is_rectangle and not is_grid:
            cv2.drawContours(contour_image, [contour], 0, (0, 0, 255), 3)
        elif shape == "X" and not is_rectangle and not is_grid:
            cv2.drawContours(contour_image, [contour], 0, (0, 255, 0), 3)
        else:
            cv2.drawContours(contour_image, [contour], 0, (64, 128, 255), 3)

    cv2.imshow("title", contour_image)
    cv2.waitKey()


def get_object_shape(solidity):
    if solidity > 0.9:
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


if __name__ == "__main__":
    image = cv2.imread("./assets/4.png")
    image = cv2.resize(image, (800, 800))
    get_tictactoe_from_image(image)
