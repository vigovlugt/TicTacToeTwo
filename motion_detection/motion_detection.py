from time import time
import cv2

MOVED_THRESHOLD = 0.1
LOCKED_TIME = 1


class MotionDetection:
    def __init__(self):
        self.last_image = None
        self.last_moved = time.now()

    def process_image(self, new_image):
        moved = self.image_has_moved(self.last_image, new_image)
        self.last_image = new_image

        if moved:
            self.last_moved = time.now()

        return self.is_locked()

    def is_locked(self):
        cur_time = time.now()

        return (cur_time - self.last_moved) > LOCKED_TIME

    def image_has_moved(self, last_image, new_image):
        return self.get_moved_value(last_image, new_image) > MOVED_THRESHOLD

    def get_moved_value(self, last_image, new_image):
        if last_image is None:
            return 1

        return cv2.matchTemplate(last_image, new_image, cv2.TM_CCOEFF_NORMED)[1]
