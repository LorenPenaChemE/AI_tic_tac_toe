"""
AI tic-tac-toe player
"""

import copy
import random
import time
from abc import ABC, abstractmethod
from enum import Enum
import string


# GameBoardPlayer probably should be an inner class of GameBoard, but because
# GameBoard class is introduced later (after studying inheritance/ABC),
# GameBoardPlayer is a standalone enum class.
class GameBoardPlayer(Enum):
    """
    An enum that represents a player on a game board; it's used to denote:
    . which player occupies a space on the board (can be NONE if unoccupied)
    . which player is the winner of the game (can be DRAW)
    """
    NONE = 0
    X = 1
    O = 2
    DRAW = 3

    def __str__(self):
        if self is GameBoardPlayer.NONE:
            return " "
        else:
            return self.name


class GameBoard(ABC):
    """ An abstract class that represents a rectangular game board. """

    @abstractmethod
    def __init__(self, nrows, ncols):
        if nrows <= 0 or ncols <= 0:
            raise ValueError(f"Invalid nrows={nrows} ncols={ncols}")

    @abstractmethod
    def get_nrows(self):
        pass

    @abstractmethod
    def get_ncols(self):
        pass

    @abstractmethod
    def set(self, row, col, value):
        pass

    @abstractmethod
    def get(self, row, col):
        pass


    def __str__(self):
        s = ""
        for row in range(self.get_nrows()):
            # The row
            s += "|".join([str(self.get(row, col)) for col in range(self.get_ncols())]) + "\n"

            # The separator
            if row != self.get_nrows() - 1:
                s += "-+" * (self.get_ncols() - 1) + "-\n"
        return s

    def get_row_winner(self, row):
        if self.get(row, 0) is GameBoardPlayer.NONE:
            # If the first cell in row is unoccupied, it's not a winner
            return GameBoardPlayer.NONE

        # # Using Python's set and/or all() can make code shorter
        # if all(self.get(row, 0) == self.get(row, i) for i in range(self.get_ncols())):
        #     return self.get(row, 0)
        # else:
        #     return GameBoardPlayer.NONE

        # The code here shows how to do it with plain old for loop.
        for col in range(self.get_ncols()):
            if self.get(row, 0) != self.get(row, col):
                # If any other element on the row is different from the first
                # one, there's no winner in this row
                return GameBoardPlayer.NONE

        # Every element in the row is the same as the first, so it's a winner
        return self.get(row, 0)

    def get_col_winner(self, col):
        if self.get(0, col) is GameBoardPlayer.NONE:
            return GameBoardPlayer.NONE

        for row in range(self.get_nrows()):
            if self.get(0, col) != self.get(row, col):
                return GameBoardPlayer.NONE

        return self.get(0, col)

    def get_diag_winner(self):
        if self.get_nrows() != self.get_ncols():
            return GameBoardPlayer.NONE

        # Get the winner in the \ diagonal
        upper_left = self.get(0, 0)
        if upper_left is not GameBoardPlayer.NONE:
            for row in range(self.get_nrows()):
                if upper_left != self.get(row, row):
                    break
            else:
                # If the for loop completes without break, all elements in
                # the diagonal is the same, so it's a winner
                return upper_left

        # Get the winner in the / diagonal
        upper_right = self.get(0, self.get_ncols() - 1)
        if upper_right is not GameBoardPlayer.NONE:
            col = self.get_ncols() - 1
            for row in range(self.get_nrows()):
                if upper_right != self.get(row, col):
                    break
                col -= 1
            else:
                return upper_right

        return GameBoardPlayer.NONE

    def check_for_draw(self):
        for row in range(self.get_nrows()):
            for col in range(self.get_ncols()):
                if self.get(row, col) is GameBoardPlayer.NONE:
                    # If any space is unoccupied, it's not a draw
                    return GameBoardPlayer.NONE

        return GameBoardPlayer.DRAW

    def get_winner(self):
        # Check for horizontal rows
        for row in range(self.get_nrows()):
            winner = self.get_row_winner(row)
            if winner is not GameBoardPlayer.NONE:
                return winner

        # Check for vertical columns
        for col in range(self.get_ncols()):
            winner = self.get_col_winner(col)
            if winner is not GameBoardPlayer.NONE:
                return winner

        # Check for diagonal if it's a square
        winner = self.get_diag_winner()
        if winner is not GameBoardPlayer.NONE:
            return winner

        # Finally, check for ties
        winner = self.check_for_draw()
        if winner is GameBoardPlayer.DRAW:
            return winner

        return GameBoardPlayer.NONE

    def get_all_moves(self):
        testlist = []
        for row in range(self.get_nrows()):
            for col in range(self.get_ncols()):
                if self.get(row, col) is GameBoardPlayer.NONE:
                    testlist.append((row,col))
        return testlist




class ArrayGameBoard(GameBoard):
    """A class that represents a rectangular game board using list of lists"""

    def __init__(self, nrows, ncols):
        super().__init__(nrows, ncols)
        self.board = [[GameBoardPlayer.NONE for _ in range(ncols)] for _ in range(nrows)]

    def get_nrows(self):
        return len(self.board)

    def get_ncols(self):
        return len(self.board[0])

    def set(self, row, col, value):
        # No need to validate row/col ourselves; Python list[][] does that.
        self.board[row][col] = value

    def get(self, row, col):
        return self.board[row][col]


class BitGameBoard(GameBoard):
    """A class that represents a rectangular game board using bits in an int"""

    VALUE_WIDTH = 2
    # The mask has 2 bits
    MASK = 0b11

    def __init__(self, nrows, ncols):
        super().__init__(nrows, ncols)
        self.nrows = nrows
        self.ncols = ncols
        self.board = 0

    def get_nrows(self):
        return self.nrows

    def get_ncols(self):
        return self.ncols

    def get_pos(self, row, col):
        """Get the bit position for row/col"""
        return (row * self.get_ncols() + col) * self.VALUE_WIDTH

    def validate(self, row, col):
        if not (0 <= row < self.nrows and 0 <= col < self.ncols):
            raise IndexError(f"Invalid row={row}, col={col}")

    def set(self, row, col, player):
        self.validate(row, col)
        pos = self.get_pos(row, col)
        self.board &= ~(self.MASK << pos)
        # Use player.value to convert enum member to an int so it can be stored
        # in self.board.
        self.board |= player.value << pos

    def get(self, row, col):
        self.validate(row, col)
        pos = self.get_pos(row, col)
        # Use GameBoardPlayer(int) to convert int (that's stored the board)
        # to an enum member.
        return GameBoardPlayer((self.board >> pos) & self.MASK)


# TODO OPTIONAL Implement and test a game board that uses numpy array
class NumpyGameBoard(GameBoard):
    """A class that represents a rectangular game board using numpy array"""

    def __init__(self, nrows, ncols):
        pass

    def get_nrows(self):
        pass

    def get_ncols(self):
        pass

    def set(self, row, col, value):
        pass

    def get(self, row, col):
        pass

class TicTacToeBoard:
    """A class that represents a 3x3 tic-tac-toe game board"""
    NROWS = 3
    NCOLS = 3

    def __init__(self):
        self.board = ArrayGameBoard(self.NROWS, self.NCOLS)


    def set(self, row, col, value):
        if self.board.get(row, col) != GameBoardPlayer.NONE:
            raise ValueError(f"{row} {col} already has {self.board.get(row, col)}")
        self.board.set(row, col, value)

    def get(self, row, col):
        return self.board.get(row, col)

    def get_winner(self):
        return self.board.get_winner()

    def get_all_moves(self):
        return self.board.get_all_moves()

    def __str__(self):
        return self.board.__str__()


class HumanPlayer:
    """ A class that represents a human player """

    def __init__(self, side):
        self.side = side

    def __str__(self):
        return f"Human player {self.side}"

    def get_move(self, board):
        while True:
            try:
                moves = input(f"Please input move for {self} (row column): ")
                row, col = moves.split()
                return int(row), int(col)
            except Exception as e:
                print("Invalid input")


class AiPlayer:
    #height of node is important
    def __init__(self, side):
        self.side = side

    def __str__(self):
        return f"AI Player {self.side}"

    def get_move(self, board):
        while True:
            try:
                side, move = self.recursive_func(board, self.side)
                row = move[0]
                col = move[1]
                return row, col
            except Exception as e:
                print(str(e))

    def recursive_func(self, board, side):
        check_first_win = board.get_winner()
        if check_first_win is not GameBoardPlayer.NONE:
            return check_first_win, None
        for move in board.get_all_moves():
            row = move[0]
            col = move[1]
            board_copy = copy.deepcopy(board)
            board_copy.set(row, col, side)
            if side  == GameBoardPlayer.X:
                other_side = GameBoardPlayer.O
            else:
                other_side = GameBoardPlayer.X
            win = self.recursive_func(board_copy, other_side)
            if win[0] is side:
                return side, move
            elif win[0] is GameBoardPlayer.DRAW:
                return win[0], move
            #move is inside win[1]

        return win[0], random.choice(board.get_all_moves())


def validate_player(player1, player2):
    """ Validates the two players playing the game """
    if player1.side is player2.side:
        raise ValueError(f"Players should not be one the same side {player1.side}")


def ttt_game(player_x, player_o):
    """
    Play a round of Tic Tac Toe, until there's either a winner, or the game
    is a draw.
    """
    validate_player(player_x, player_o)

    ttt_board = TicTacToeBoard()
    current_player = player_x

    print("Welcome to the game Tic-tac-toe!")
    print(ttt_board)
    while True:
        # Pass the current player a copy of the board, in case the player cheats
        # and tries to modify the board
        start = time.perf_counter()
        row, col = current_player.get_move(copy.deepcopy(ttt_board))
        duration = time.perf_counter() - start
        print(f"{current_player} makes move ({row} {col}) in {duration:.3f} seconds")
        try:
            ttt_board.set(row, col, current_player.side)
        except (ValueError, IndexError) as e:
            # ValueError if the space is already occupied, IndexError if off-grid
            print(e)
            continue
        print(ttt_board)

        winner = ttt_board.get_winner()
        if winner is GameBoardPlayer.DRAW:
            print("Game is a draw")
            break
        elif winner is GameBoardPlayer.NONE:
            # Switch player
            current_player = player_x if current_player is player_o else player_o
        else:
            # There's a winner
            print(f"{current_player} wins")
            break

    return winner


def main():
    # Use the same random.seed(1) if you want to generate the same random
    # numbers each time the program is run, which is good for
    # development/testing.
    # random.seed(1)
    ttt_game(player_x=AiPlayer(GameBoardPlayer.X),
             player_o=AiPlayer(GameBoardPlayer.O))

if __name__ == '__main__':
   main()



