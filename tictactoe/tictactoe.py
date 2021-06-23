from random import choice

from PIL.Image import NONE
import numpy

PLAYERS = ["X", "O"]


class TicTacToe:
    def start(self, turn=None, board=None):
        '''
        Setup for game.
        '''
        # If turn is given and within PLAYERS, give current turn to them.
        # Else choose randomly who starts.
        if turn in PLAYERS:
            self.turn = turn
        else:
            self.turn = choice(PLAYERS)

        # If board is given, use this board. Else create a
        # 3x3 2d array as board.
        if board:
            self.board = board
        else:
            self.board = [[None] * 3 for _ in range(3)]

    def printBoard(self):
        '''
        Prints current board.
        '''
        print("\nTurn:", self.turn, end="\n\n")
        board = [[i if i else " " for i in j] for j in self.board]
        print("\n---+---+---\n".join([" " + " | ".join(row)
                                      for row in board]))

    def move(self, x, y):
        '''
        Plays a move by changing coordinate to symbol of current turn.
        '''
        self.board[y][x] = self.turn
        self.turn = "X" if self.turn == "O" else "O"

        return self.checkForWinner()

    def undo(self, x, y):
        '''
        Undo a move at given x and y coordinate.
        '''
        self.board[y][x] = None

    def possibleMoves(self):
        '''
        Return a list of coordinates of all empty places on board.
        '''
        posMoves = []

        for x in range(0, 3):
            for y in range(0, 3):
                if self.board[x][y] is None:
                    posMoves.append((y, x))
        return posMoves

    def freePos(self, x, y):
        '''
        Checks if given pos is either full (returns 1), empty (returns 0)
        or outisde of board (returns 2).
        '''
        if x > 2 or x < 0 or y > 2 or y < 0:
            return 2
        if self.board[y][x] == 'X' or self.board[y][x] == 'O':
            return 1
        else:
            return 0

    def legalMoveSet(self, board):
        '''
        Checks if one legal move is set and executes this move if so.
        '''
        moves = []

        for y in range(0, 3):
            for x in range(0, 3):
                if board[y][x] and board[y][x] != self.turn and self.board[y][x] and self.board != self.turn:
                    raise ValueError("Misplaced computer set")
                if board[y][x] == self.turn and self.board[y][x] is None:
                    moves.append((x, y))

        if len(moves) > 1:
            raise ValueError("Too much sets", moves)
        elif len(moves) == 1:
            x, y = moves[0]
            self.move(x, y)

        return False

    def checkForWinner(self):
        '''
        Check if a player has won. Returns symbol of winning player. If
        game is tie, return tie. Else return None.
        '''
        rows = (self.board +
                [[self.board[y][x] for y in range(3)] for x in range(3)] +
                [[self.board[i][i] for i in range(3)]] +
                [[self.board[i][2 - i] for i in range(3)]])

        for row in rows:
            if row[0] == row[1] == row[2] is not None:
                # After move, turns change, so winner is last turns player.
                if self.turn == 'O':
                    return 'X'
                elif self.turn == 'X':
                    return 'O'

        return None if None in numpy.array(self.board).flatten() else "tie"
