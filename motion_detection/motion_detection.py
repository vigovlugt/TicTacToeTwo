from datetime import datetime
import cv2

MOVED_THRESHOLD = 0.04
# MOVED_THRESHOLD = 0.1
LOCKED_TIME = 2.0
# LOCKED_TIME = 0.5


class MotionDetection:
    def __init__(self):
        self.last_image = None
        self.last_moved = datetime.now()
        self.last_moved_value = 0

    def process_image(self, new_image):
        moved = self.image_has_moved(self.last_image, new_image)
        self.last_image = new_image

        if moved:
            self.last_moved = datetime.now()

        return self.is_locked()

    def is_locked(self):
        cur_time = datetime.now()

        return (cur_time - self.last_moved).total_seconds() < LOCKED_TIME

    def image_has_moved(self, last_image, new_image):
        moved_value = self.get_moved_value(
            last_image, new_image)
        has_moved = abs(moved_value - self.last_moved_value) > MOVED_THRESHOLD
        self.last_moved_value = moved_value

        return has_moved

    def get_moved_value(self, last_image, new_image):
        if last_image is None:

            return 1
        x = cv2.matchTemplate(last_image, new_image, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(x)
        return max_val
