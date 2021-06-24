'''
Names: J. Boon, F. Hoetjes, J. Siegers, V. Vlugt & L. van der Waals
MM_Group: 3
Study: BSc Informatica
app.py:
    - Manages the actual Tic Tac Toe game itself.
    - It also manages the camera, wether or not the board is being detected or
      wether or not the image has moved.
    - Also manages the games state of the Tic Tac Toe game, and checks for a
      winner and prints the result.
'''

from tictactoe import ai
from tictactoe.tictactoe import TicTacToe
import image_processing.image_processing as ip
import image_processing.affine_transformation as at
import image_processing.board_recognition as br
from motion_detection.motion_detection import MotionDetection
# import sys


class Application:
    '''
    This class contains all main logic of the app. This is also the class
    which couples all other modules to work together as a whole.
    '''

    def __init__(self, difficulty, first):
        '''
        Initialize TicTacToe board, Motion Detection and player settings.
        '''
        self.ttt = TicTacToe()
        self.motion_detector = MotionDetection()
        self.game_finished = None
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
        '''
        This method gets called every webcam frame.
        It preprocesses the image, checks if app is locked by motion detection,
        gets the board, makes AI moves and returns the result board with
        projected shapes.
        '''
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

        if board is None:
            print("No board detected")
            return image

        transformed = at.get_affine_transform(board_lines, image,
                                              self.ttt.board, board)
        self.last_image = transformed

        # print(board_lines, board)


        try:
            if self.ttt.legalMoveSet(board):
                self.ttt.printBoard()
                if self.ttt.checkForWinner() in ["X", "O", "tie"]:
                    ai.result(self.ttt)
                    self.game_finished = self.ttt.checkForWinner()
                else:
                    ai.aiMove(self.ttt, self.diff)
                    self.ttt.printBoard()
                    if self.ttt.checkForWinner() in ["X", "O", "tie"]:
                        ai.result(self.ttt)
                        self.game_finished = self.ttt.checkForWinner()
        except ValueError as e:
            print(e)

        return transformed
