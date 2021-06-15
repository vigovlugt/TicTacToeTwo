import random
import tictactoe
import numpy as np
from copy import deepcopy

def easy(ttt):
    '''
    Easy difficulty AI. Chooses moves at random but it will block a players win
    and play a winning move whenever possible.
    '''
    posMoves = ttt.possibleMoves()

    if finalMove(ttt, posMoves) == 1:
        return

    pos = random.choice(posMoves)
    ttt.move(int(pos[0]), int(pos[1]))

def finalMove(ttt, posMoves):
    '''
    Try every possible move and check if AI wins. If AI cannnot win, try
    every possible move for player and check if player wins. If player can win
    then play that move with AI to block win.
    '''
    for pos in posMoves:
        ttt.move(int(pos[0]), int(pos[1]))

        if ttt.checkForWinner() == 'O':
            return 1

        ttt.move(int(pos[0]), int(pos[1]))

        if ttt.checkForWinner() == 'X':
            ttt.undo(int(pos[0]), int(pos[1]))
            ttt.move(int(pos[0]), int(pos[1]))
            return 1

        ttt.undo(int(pos[0]), int(pos[1]))

def medium(ttt):
    '''
    Medium difficulty AI. Blocks the players winning move and it will play a
    winning move whenever possible. Else if center is free, plays in center.
    Then plays random corner and if all corners are full, plays a random edge.
    '''
    posMoves = ttt.possibleMoves()

    if finalMove(ttt, posMoves) == 1:
        return

    if (1,1) in posMoves:
        ttt.move(1,1)
        return

    if moveCorner(ttt, posMoves) == 1:
        return

    moveEdge(ttt, posMoves)

def moveCorner(ttt, posMoves):
    '''
    Creates list of all free corners and plays a random one. If no free
    corners are found, return 0.
    '''
    freeCorners = []
    for pos in posMoves:
        if pos in [(0,0), (0,2), (2,0), (2,2)]:
            freeCorners.append(pos)

    if len(freeCorners) > 0:
        move = random.choice(freeCorners)
        ttt.move(move[0], move[1])
        return 1
    else:
        return 0

def moveEdge(ttt, posMoves):
    '''
    Creates list of all free edges and plays a random one. If no free
    edges are found, return 0.
    '''
    freeEdges = []
    for pos in posMoves:
        if pos in [(1,0), (0,1), (2,1), (1,2)]:
            freeEdges.append(pos)

    if len(freeEdges) > 0:
        move = random.choice(freeEdges)
        ttt.move(move[0], move[1])
        return 1
    else:
        return 0

def hard(ttt):
    '''
    Most difficult AI. Uses a minimax algorithm to determine
    a score per move and then plays the move with the best score.
    Impossible to win from.
    '''
    bestScore = -2
    bestMove = 0

    posMoves = ttt.possibleMoves()

    # Empty board, so corner move is best move, no need for algorithm.
    if len(posMoves) == 9:
        ttt.move(0,0)
        return

    # Copy board, try move, recursively finish game and determine score.
    # Best scoring move gets played.
    for pos in posMoves:
        tttcopy = deepcopy(ttt)
        tttcopy.move(int(pos[0]), int(pos[1]))
        score = minimax(tttcopy, False)
        tttcopy.undo(int(pos[0]), int(pos[1]))
        if score > bestScore:
            bestScore = score
            bestMove = pos

    ttt.move(bestMove[0], bestMove[1])

def minimax(ttt, maximize):
    '''
    Minimax algorithm. Tries a move and then checks it's score by recursively
    playing moves until the game is finished, then determining the score by
    checking who won or if game ended in tie.
    '''
    if ttt.checkForWinner() == 'O':
        return 1
    elif ttt.checkForWinner() == 'X':
        return -1
    elif ttt.checkForWinner() == 'tie':
        return 0

    # Maximizing is AI, minimizing is player.
    if maximize:
        bestScore = -2
        posMoves = ttt.possibleMoves()
        for pos in posMoves:
            tttcopy = deepcopy(ttt)
            tttcopy.move(int(pos[0]), int(pos[1]))
            score = minimax(tttcopy, False)
            tttcopy.undo(int(pos[0]), int(pos[1]))
            if score > bestScore:
                bestScore = score
        return bestScore
    else:
        bestScore = 2
        posMoves = ttt.possibleMoves()
        for pos in posMoves:
            tttcopy = deepcopy(ttt)
            tttcopy.move(int(pos[0]), int(pos[1]))
            score = minimax(tttcopy, True)
            tttcopy.undo(int(pos[0]), int(pos[1]))
            if score < bestScore:
                bestScore = score
        return bestScore

def playerMove(ttt):
    '''
    Allows for the player to make a move by giving an x and y value between 1
    and 3, corresponding to a coordinate in the grid.
    '''
    while ttt.turn == 'X':
        try:
            x = int(input("\nGive a X coordinate (1-3): ")) - 1
            y = int(input("Give a Y coordinate (1-3): ")) - 1
        except:
            print("Invalid input, please try again.")
            return -1

        if ttt.freePos(x, y) == 0:
            ttt.move(x,y)
        elif ttt.freePos(x, y) == 1:
            print("Position is already occupied, please try again.")
        elif ttt.freePos(x, y) == 2:
            print("Position is invalid, please try again.")

def aiMove(ttt, diff):
    '''
    Plays move using AI determined by diff value given at start.
    '''
    if diff == '1':
        easy(ttt)
    elif diff == '2':
        medium(ttt)
    elif diff == '3':
        hard(ttt)

def result(ttt):
    '''
    Display the final results of the game.
    '''
    if ttt.checkForWinner() == 'X':
        print("\nYou win!")
    elif ttt.checkForWinner() == 'O':
        print("\nYou lose.")
    else:
        print("\nTie game.")

def main():
    '''
    Contains configuration for AI difficulty and who goes first. Then
    enters game loop until winner or tie is determined.
    '''
    ttt = tictactoe.TicTacToe()

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
    while ttt.checkForWinner() == None:
        ttt.printBoard()
        if ttt.turn == 'X':
            while playerMove(ttt) == -1:
                playerMove(ttt)
        else:
            aiMove(ttt, diff)

    # Print final board and show result.
    ttt.printBoard()
    result(ttt)


if __name__ == '__main__':
    main()