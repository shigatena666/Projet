from copy import deepcopy
from action import Action

import numpy as np

import utilities


X = "X"
O = "O"
EMPTY = ' '


class Board:

    def __init__(self, first_player='X', array=None):

        # set the first player in the board.
        self.__first_player = first_player

        # check if a parameter has been provided.
        if array is not None:
            self.__array = deepcopy(array)
            return

        # if there is no parameter, create an empty board of 3x3.
        self.__array = deepcopy(utilities.initial_state())

    def get_initial_player(self):

        # get the char of the first player.
        return self.__first_player

    def get_current_game_state(self):

        # get the array of the game.
        return self.__array

    def current_player(self):

        # check if the board state is still the same as the beginning. If it is the case,
        # the defined player in ctor should play first.
        if (self.__array == utilities.initial_state()).all():
            return self.__first_player

        # let's count how many xs and os there is in the game.
        x_counter = 0
        o_counter = 0

        # iterate through our lines and columns.
        for row in range(len(self.__array)):
            for column in range(len(self.__array[row])):

                # add one to our counters if we meet the player.
                if self.__array[row][column] == X:
                    x_counter += 1
                elif self.__array[row][column] == O:
                    o_counter += 1

        # we will use the property that the first player needs to play again when the other player
        # has the same amount of plays.
        if x_counter == o_counter:
            return self.__first_player
        else:
            return O if self.__first_player == X else X

    def get_allowed_actions(self):

        # prepare an array of actions.
        actions = []

        # iterate through all elements.
        for row in range(len(self.__array)):
            for column in range(len(self.__array[row])):

                # check if the element is set or not.
                if self.__array[row][column] != EMPTY:
                    continue

                # if it's not set, then there is a possibility to play on that slot.
                # create a list to store the action and append it to the list.
                actions.append(Action(row, column))

        # return our array of actions.
        return np.array(actions)

    def __set(self, line, column):

        # set the slot to the player who needs to play.
        self.__array[line][column] = self.current_player()

    def result(self, action: Action):

        if self.__array[action.get_x()][action.get_y()] != EMPTY:
            raise Exception('The slot is already occupied, this should not occur.')

        # create a deep-copy of the board.
        new_board = Board(self.__first_player, self.__array)

        # set the actions and return the new board.
        new_board.__set(action.get_x(), action.get_y())

        # return the new board.
        return new_board

    def winner(self):

        # let's look into the lines.
        for line in range(len(self.__array)):

            # create a set for the line.
            line_set = set(self.__array[line])

            # if the length is 1 and the first character isn't a space then it means someone won.
            if len(line_set) == 1 and EMPTY not in line_set:
                return X if self.__array[line][0] == X else O

        # let's look into the columns, use the property of a matrix to make it easier.
        transpose = np.transpose(self.__array)

        for line in range(len(transpose)):

            # create a set for the transpose.
            transpose_set = set(transpose[line])

            # if the length is 1 and the first character isn't a space then it means someone won.
            if len(transpose_set) == 1 and EMPTY not in transpose_set:
                return X if transpose[line][0] == X else O

        # check for diagonals and create our sets.
        descending_diagonal_set = set([self.__array[i][i] for i in range(len(self.__array))])
        ascending_diagonal_set = set([self.__array[i][len(self.__array[i]) - 1 - i] for i in range(0, len(self.__array))])

        # return the player in the diagonal that has won if there is any.
        if len(descending_diagonal_set) == 1 and EMPTY not in descending_diagonal_set:
            return X if self.__array[0][0] == X else O

        # same thing.
        if len(ascending_diagonal_set) == 1 and EMPTY not in ascending_diagonal_set:
            return X if self.__array[0][2] == X else O

        # check for equality.
        return None

    def has_game_ended(self):

        # let's check if the board is full or if there is a winner.
        return True \
            if ((self.__array != utilities.initial_state()).all() or self.winner() is not None) \
            else False

    def who_has_won(self):

        # get the winner.
        who_won = self.winner()

        # check who it is and return an integer based on this.
        if who_won == X:
            return 1
        elif who_won == O:
            return -1
        else:
            return 0

    def __str__(self):
        st = '_______\n'
        for i in range(len(self.__array)):
            st += '|'
            st += '|'.join(self.__array[i])
            st += '|\n'
        st += '_______'
        return st