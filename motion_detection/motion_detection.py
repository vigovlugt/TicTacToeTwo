'''
Names: J. Boon, F. Hoetjes, J. Siegers, V. Vlugt & L. van der Waals
MM_Group: 3
Study: BSc Informatica
motion_detection.py:
    - This program acts as a motion detector.
    - It utilizes a MOVED_THRESHHOLD which is how much the image can move
      before it gets "locked" (in a locked state the board will not be read).
    - The LOCKED_TIME variable is the time that board will remain in a locked
      state.
'''

from datetime import datetime
import cv2

MOVED_THRESHOLD = 0.04
# MOVED_THRESHOLD = 0.1
LOCKED_TIME = 1.0
# LOCKED_TIME = 0.5


class MotionDetection:
    def __init__(self):
        self.last_image = None
        self.last_moved = datetime.now()
        self.last_moved_value = 0

    def process_image(self, new_image):
        '''
        Takes a new image and processes it. If any image has moved in
        the last second, returns False, which tells the main loop that
        it should not detect the board in the new image.
        '''
        moved = self.image_has_moved(self.last_image, new_image)
        self.last_image = new_image

        if moved:
            self.last_moved = datetime.now()

        return self.is_locked()

    def is_locked(self):
        '''
        Function for putting the camera in a "locked" state. In the locked
        state no new images will be read.
        '''
        cur_time = datetime.now()

        return (cur_time - self.last_moved).total_seconds() < LOCKED_TIME

    def image_has_moved(self, last_image, new_image):
        '''
        Detects wether or not the camera image has moved.
        '''
        moved_value = self.get_moved_value(
            last_image, new_image)
        has_moved = abs(moved_value - self.last_moved_value) > MOVED_THRESHOLD
        self.last_moved_value = moved_value

        return has_moved

    def get_moved_value(self, last_image, new_image):
        '''
        Get a value which tells how much the image has moved
        when compared to the last image.
        '''
        if last_image is None:

            return 1
        x = cv2.matchTemplate(last_image, new_image, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(x)
        return max_val
