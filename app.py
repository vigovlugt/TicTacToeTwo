from tictactoe import ai
from tictactoe.tictactoe import TicTacToe
import image_processing.image_processing as ip
from motion_detection.motion_detection import MotionDetection
import sys


class Application:
    def __init__(self, difficulty, first):
        self.ttt = TicTacToe()
        self.motion_detector = MotionDetection()

        args = sys.argv

        # Choose AI difficulty.
        if difficulty == "Easy":
            diff = 1
        elif difficulty == "Medium":
            diff = 2
        elif difficulty == "Hard":
            diff = 3

        # Choose starting player.
        if first == 'Player':
            self.ttt.start('X')
        elif first == 'AI':
            self.ttt.start('O')

    def update(self, image):
        is_locked = self.motion_detector.process_image(image)

        if is_locked:
            print("Image has moved in last second, app locked")
            return image

        board, contour_image = ip.get_tictactoe_from_image(image)
        if board is None:
            print("No board detected")
            return contour_image

        if self.ttt.legalMoveSet(board):
            print("Legal move is set on the board")
            ip.print_board(board)
            ai.aiMove(ttt, diff)
            return contour_image
