# Author: Brent Goldman
# Date: 5/22/2021
# Description: This program allows users to play a game called Orthokon.
#              The game consists of a 4x4 board with 4 red pieces on one
#              end, and 4 yellow pieces on the other end.  The user can
#              move a piece in either an orthogonal or diagonal direction.
#              A piece will move as far as it can go until it either hits
#              another piece or hits the edge of the board.  If their
#              are any pieces of a different color that are orthogonal to the
#              piece moved, then those pieces are changed into the color of
#              the piece moved.  The game is over when a player has no
#              available moves, i.e. they are blocked on all sides for all
#              their pieces, or if all the pieces are of one color.


class OrthokonBoard:
    """Creates the Orthokon Board, makes valid moves, updates the board after
    moves, and update the game status for a winner"""

    def __init__(self):
        """Creates data members to be used in the game"""

        # Board data member is a list of lists.  First list is row 0 on the
        # board, second list is row 1 on the board,...
        # First item of a list is column 0, then column 1, ....
        # To check row and column, use self._board[row][column].
        self._board = [["R", "R", "R", "R"], ["", "", "", ""], ["", "", "", ""],
                       ["Y", "Y", "Y", "Y"]]
        self._current_state = "UNFINISHED"
        self._move_counter = 0

    def get_current_state(self):
        """Returns the current state of the game: UNFINISHED, RED_WON
        YELLOW_WON"""
        return self._current_state

    def make_move(self, start_row, start_column, end_row, end_column):
        """Accepts arguments for where to move a piece.  Validate the
        move is acceptable.  Make the move if it is acceptable.  Flip over
        opponents pieces that are orthogonal.  Update the status of the game
        if it has changed."""

        # Check that starting row / column, and end row / column are in range
        if start_row not in range(0, 4) or start_column not in range(0, 4) or \
                end_row not in range(0, 4) or end_column not in range(0, 4):
            print("Request not in range")
            return False

        # Determine which direction for move
        row_direction = end_row - start_row
        column_direction = end_column - start_column

        # If row_direction and column_direction are zero than move is invalid
        # since the piece is not being moved.
        if row_direction == 0 and column_direction == 0:
            print("Requested zero move size")
            return False

        # Make sure there is a piece in the start row,column.
        # Save the color of the piece being moved.
        if self._board[start_row][start_column] == "":
            print("Requested empty space to move")
            return False
        else:
            color = self._board[start_row][start_column]

        # Use intermediate variables to check whether a row,column is
        # occupied.  Initialize variables to start row, column.
        check_row = start_row
        check_column = start_column

        # Keep track of where the piece is.  Initialize to start row,column.
        current_row = start_row
        current_column = start_column

        # Use status variable to determine when to stop moving the piece.
        status = "OK"

        # Keep track of spaces moved.  To be valid, a move must be at least
        # one space.
        spaces_moved = 0

        # Determine how far the piece can move.  We want to make sure the
        # piece can move as far as it can go before it either hits the edge
        # of the board or another piece.
        while status == "OK":
            # Determine which row to try and move the piece
            if row_direction > 0:
                check_row += 1
            elif row_direction < 0:
                check_row -= 1
            # Determine which column to try and move the piece
            if column_direction > 0:
                check_column += 1
            elif column_direction < 0:
                check_column -= 1
            # Check to make sure the piece can move to the next space,
            # by validating the space is empty and it's on the board
            if check_row not in range(0, 4) or check_column not in range(0, 4) \
                    or self._board[check_row][check_column] != "":
                # Update status of move to NOT_OK since the piece can not
                # move into the requested row,column.
                status = "NOT_OK"
                # If the piece moved zero spaces return False
                # Else set the final row, column for the piece
                if spaces_moved == 0:
                    print("Unable to move 1 space")
                    return False
            # Update the current location
            else:
                spaces_moved += 1
                current_row = check_row
                current_column = check_column

        # Update the board if current location equals end location
        # If current location does not equal end location then one of the
        # following is true; return false:
        #   -The piece could not move the entire distance.
        #   -The piece could have moved further than requested.
        #   -The location requested to move is not on an orthogonal or
        #   diagonal.
        if current_row == end_row and current_column == end_column:
            self._board[end_row][end_column] = color
            self._board[start_row][start_column] = ""
            self._move_counter += 1
        else:
            print("End location is not allowed.")
            return False

        # Flip any orthogonal pieces that are not the same color as the piece
        # moved.  Orthogonal is left/right or up/down, not diagnonal.
        # Up to four orthoganl spaces to check in relation to current space,
        # [-1, 0], [0, -1], [+1, 0], [0, +1]
        # Only check the space though if it's on the board!
        for row in range(-1, 2, 1):
            if 0 <= end_row + row <= 3:
                if self._board[end_row + row][end_column] != color \
                        and self._board[end_row + row][end_column] != "":
                    self._board[end_row + row][end_column] = color
        for column in range(-1, 2, 1):
            if 0 <= end_column + column <= 3:
                if self._board[end_row][end_column + column] != color \
                        and self._board[end_row][end_column + column] != "":
                    self._board[end_row][end_column + column] = color

                    # Update game status
        # Check if all pieces are of one color
        red = 0
        yellow = 0
        for list in self._board:
            for value in list:
                if value == "R":
                    red += 1
                elif value == "Y":
                    yellow += 1
        if red == 8:
            self._current_state = "RED_WON"
        elif yellow == 8:
            self._current_state = "YELLOW_WON"

        # Check if either player has no move
        # Loop through each list and if the index has a R or Y then check
        # all neighboring locations to make sure one if empty.
        current_row = 0
        red_moves = 0
        yellow_moves = 0
        for list in self._board:
            current_column = 0
            for value in list:
                color = value
                if color != "":
                    for row in range(-1, 2):
                        for column in range(-1, 2):
                            if 0 <= current_row + row <= 3 and \
                                    0 <= current_column + column <= 3:
                                if self._board[current_row + row][current_column \
                                                                  + column] == "":
                                    if color == "R":
                                        red_moves += 1
                                    else:
                                        yellow_moves += 1
                # print(current_row,current_column)
                current_column += 1
            current_row += 1
        if red == 8 or yellow_moves == 0:
            self._current_state = "RED_WON"
        elif yellow == 8 or red_moves == 0:
            self._current_state = "YELLOW_WON"

        return True

    def get_board(self):
        """Return the current board configuration"""
        return self._board

    def get_moves(self):
        """Return the number of valid moves made"""
        return self._move_counter