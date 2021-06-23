from tictactoe import ai
from tictactoe.tictactoe import TicTacToe
import image_processing.image_processing as ip
import image_processing.affine_transformation as at
import image_processing.board_recognition as br
from motion_detection.motion_detection import MotionDetection
import sys


class Application:
    def __init__(self, difficulty, first):
        self.ttt = TicTacToe()
        self.motion_detector = MotionDetection()
        self.game_finished = False
        # args = sys.argv

        # Choose AI difficulty.

        self.diff = difficulty

        # Choose starting player.
        if first == 'Player':
            self.ttt.start('X')
        elif first == 'AI':
            self.ttt.start('O')

    def update(self, image):
        pre_image = ip.preprocess_image(image)

        if self.motion_detector.process_image(pre_image):
            # print("Image has moved in last second, app locked")
            return image

        # board, contour_image = ip.get_tictactoe_from_image(image)
        shapes = ip.get_shapes(pre_image)

        board_lines = ip.get_board_lines(pre_image, shapes)
        if board_lines is None:
            print("No board lines detected")
            return image

        transformed = at.get_affine_transform(board_lines, image,
                                              self.ttt.board)
        board = br.get_board(board_lines, shapes)

        # print(board_lines, board)

        if board is None:
            print("No board detected")
            return transformed

        if self.ttt.legalMoveSet(board):
            self.ttt.printBoard()
            if self.ttt.checkForWinner() in ["X", "O"]:
                ai.result(self.ttt)
                self.game_finished = True
            else:
                ai.aiMove(self.ttt, self.diff)
                self.ttt.printBoard()
                if self.ttt.checkForWinner() in ["X", "O"]:
                    ai.result(self.ttt)
                    self.game_finished = True
        return transformed



# def print_board(board):
#     for y in range(3):
#         for x in range(3):
#             if board[y][x] is not None:
#                 print(board[y][x], end="")
#             else:
#                 print(" ", end="")
#         print()
