from tictactoe import ai
from tictactoe.tictactoe import TicTacToe
import image_processing.image_processing as ip
import image_processing.board_recognition as br
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

        self.diff = diff

        # Choose starting player.
        if first == 'Player':
            self.ttt.start('X')
        elif first == 'AI':
            self.ttt.start('O')

    def update(self, image):
        pre_image = ip.preprocess_image(image)

        if self.motion_detector.process_image(pre_image):
            print("Image has moved in last second, app locked")
            return image

        # board, contour_image = ip.get_tictactoe_from_image(image)
        shapes = ip.get_shapes(pre_image)

        board_lines = ip.get_board_lines(pre_image, shapes)
        if board_lines is None:
            print("No board lines detected")
            return

        board = br.get_board(board_lines, shapes)

        print(shapes, board_lines, board)

        if board is None:
            print("No board detected")
            return

        if self.ttt.legalMoveSet(board):
            print("Legal move is set on the board:")
            ip.print_board(board)
            ai.aiMove(self.ttt, self.diff)
            print("AFTER AI:")
            ip.print_board(board)
            return
