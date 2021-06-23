from tictactoe import ai
from tictactoe.tictactoe import TicTacToe
import image_processing.image_processing as ip
import image_processing.affine_transformation as at
import image_processing.board_recognition as br
from motion_detection.motion_detection import MotionDetection
# import sys


class Application:
    def __init__(self, difficulty, first):
        self.ttt = TicTacToe()
        self.motion_detector = MotionDetection()
        self.game_finished = False
        self.last_image = None
        # args = sys.argv

        # Choose AI difficulty.

        self.diff = difficulty

        # Choose starting player.
        if first == 'Player':
            self.ttt.start('X')
        elif first == 'AI':
            self.ttt.start('O')
            ai.aiMove(self.ttt, self.diff)

    def update(self, image):
        pre_image = ip.preprocess_image(image)

        if self.motion_detector.process_image(pre_image):
            print("Image has moved in last second, app locked")
            if self.last_image is None:
                return image
            else:
                return self.last_image

        # board, contour_image = ip.get_tictactoe_from_image(image)
        shapes = ip.get_shapes(pre_image)

        board_lines = ip.get_board_lines(pre_image, shapes)
        if board_lines is None:
            print("No board lines detected")
            return image

        board = br.get_board(board_lines, shapes)
        transformed = at.get_affine_transform(board_lines, image,
                                              self.ttt.board, board)
        self.last_image = transformed

        # print(board_lines, board)

        if board is None:
            print("No board detected")
            return transformed

        try:
            if self.ttt.legalMoveSet(board):
                self.ttt.printBoard()
                if self.ttt.checkForWinner() in ["X", "O", "tie"]:
                    ai.result(self.ttt)
                    self.game_finished = True
                else:
                    ai.aiMove(self.ttt, self.diff)
                    self.ttt.printBoard()
                    if self.ttt.checkForWinner() in ["X", "O", "tie"]:
                        ai.result(self.ttt)
                        self.game_finished = True
        except ValueError as e:
            print(e)

        return transformed
