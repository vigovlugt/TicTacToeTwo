from random import choice
import numpy

PLAYERS = ["X", "O"]

class TicTacToe:
    def start(self, turn = None, board = None):
        if turn in PLAYERS:
            self.turn = turn
        else:
            self.turn = choice(PLAYERS)

        if board:
            self.board = board
        else:
            self.board = [[" "] * 3 for _ in range(3)]

    def printBoard(self):
        """
        Voor het testen in de terminal
        """
        print("Turn:", self.turn, end="\n\n")
        print("\n---+---+---\n".join([" " + " | ".join(row)
                                      for row in self.board]))

    def move(self, x, y):
        self.board[y][x] = self.turn
        self.turn = "X" if self.turn == "O" else "O"

        return self.checkForWinner()

    def checkForWinner(self):
        rows = self.board + [[self.board[y][x] for y in range(3)] for x in range(3)] + [[self.board[i][i] for i in range(3)]] + [[self.board[i][2 - i] for i in range(3)]]
        for row in rows:
            if row[0] == row[1] == row[2] != " ":
                return[0]

        return None if " " in numpy.array(self.board).flatten() else "tie"
