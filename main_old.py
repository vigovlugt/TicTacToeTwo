from tictactoe import ai
from tictactoe.tictactoe import TicTacToe
import image_processing.image_processing as ip


def main():
    '''
    Contains configuration for AI difficulty and who goes first. Then
    enters game loop until winner or tie is determined.
    '''
    ttt = TicTacToe()

    # Choose AI difficulty.
    diff = input("\nChoose AI difficulty (1: Easy, 2: Medium, 3: Hard): ")
    while diff != '1' and diff != '2' and diff != '3':
        diff = input("Please try again (1: Easy, 2: Medium, 3: Hard): ")

    # Choose starting player.
    first = input("Go first? [y/n]: ").lower()
    while first != 'y' and first != 'n':
        first = input("Please try again [y/n]: ").lower()

    if first == 'y':
        ttt.start('X')
    elif first == 'n':
        ttt.start('O')

    # Game loop.
    while ttt.checkForWinner() is None:
        ttt.printBoard()
        if ttt.turn == 'X': # Player turn

            # Loop until board in image is different
            # than current board.
            while True:
                img =  ip.get_photo()
                board = ip.get_tictactoe_from_image(img)
                if ttt.cmpBoard(board):
                    break
        else: # AI turn
            ai.aiMove(ttt, diff)

    # Print final board and show result.
    ttt.printBoard()
    ai.result(ttt)


if __name__ == '__main__':
    main()