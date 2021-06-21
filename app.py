from tictactoe import ai
from tictactoe.tictactoe import TicTacToe
import image_processing.image_processing as ip
from motion_detection.motion_detection import MotionDetection
import sys


class Application:
    def __init__(self):
        self.ttt = TicTacToe()
        self.motion_detector = MotionDetection()

        args = sys.argv

        # Choose AI difficulty.
        diff = args[1] if len(args) == 3 else input(
            "\nChoose AI difficulty (1: Easy, 2: Medium, 3: Hard): ")
        while diff != '1' and diff != '2' and diff != '3':
            diff = input("Please try again (1: Easy, 2: Medium, 3: Hard): ")

        # Choose starting player.
        first = args[2] if len(args) == 3 else input(
            "Go first? [y/n]: ").lower()
        while first != 'y' and first != 'n':
            first = input("Please try again [y/n]: ").lower()

        if first == 'y':
            self.ttt.start('X')
        elif first == 'n':
            self.ttt.start('O')

    def update(self, image):
        image = ip.preprocess_image(image)

        is_locked = self.motion_detector.process_image(image)

        if is_locked:
            print("Image has moved in last second, app locked")
            return

        board = ip.get_tictactoe_from_image(image)
        if board is None:
            print("No board detected")
            return

        if self.ttt.equal(board):
            print("Board is still equal")
            return

        ip.print_board(board)
