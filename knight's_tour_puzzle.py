# Helper function for splitting input into two integers
def valid_position(x):
    """
    Validates and splits input string into two integers.

    Args:
        x (str): The input string.

    Returns:
        list: A list containing two integers if the input is valid, otherwise 0.
    """
    try:
        x = str(x)
        x = x.split(" ")
        assert len(x) == 2
        return [int(x[0]), int(x[1])]
    except (ValueError, AssertionError):
        return 0

# Function to handle the starting message and initial input
def starting_messages():
    """
    Prompts the user for board dimensions, knight's starting position, and choice to try the puzzle.

    Returns:
        tuple: A tuple containing the row position, column position, row dimension, column dimension, and puzzle choice.
    """
    # Loop to get valid board dimensions
    while True:
        x = input("Enter your board dimensions: ")
        dimensions = valid_position(x)
        try:
            assert 1 <= dimensions[0] and 1 <= dimensions[1]
            break
        except (ValueError, AssertionError, TypeError):
            print("Invalid dimensions!")

    # Loop to get valid knight's starting position
    while True:
        x = input("Enter the knight's starting position: ")
        pos = valid_position(x)
        try:
            assert 1 <= pos[0] <= dimensions[0] and 1 <= pos[1] <= dimensions[1]
            break
        except (ValueError, AssertionError, TypeError):
            print("Invalid dimensions!")

    # Loop to get user's choice to try the puzzle or not
    while True:
        x = input("Do you want to try the puzzle? (y/n): ")
        if x == 'y':
            return pos[1], pos[0], dimensions[1], dimensions[0], False
        if x == 'n':
            return pos[1], pos[0], dimensions[1], dimensions[0], True
        print("Invalid input!")

# Function to determine if a solution exists for the given board dimensions
def solution_exists(row_n, col_n):
    """
    Checks if a solution exists for the given board dimensions.

    Args:
        row_n (int): The number of rows on the board.
        col_n (int): The number of columns on the board.

    Returns:
        bool: True if a solution exists, False otherwise.
    """
    # Assign lesser and more based on row_n and col_n
    less, more = (row_n, col_n) if row_n < col_n else (col_n, row_n)

    # Check the conditions for which no solution exists
    if less == 1 or less == 2 or (less == 3 and (more == 3 or more == 5 or more == 6)) or (less == 4 and more == 4):
        return False
    return True

# Class definition for Game
class Game:
    def __init__(self, row_pos, col_pos, row_n, col_n, ai):
        """
        Initializes a Game object.

        Args:
            row_pos (int): The starting row position of the knight.
            col_pos (int): The starting column position of the knight.
            row_n (int): The dimension of the board (number of rows).
            col_n (int): The dimension of the board (number of columns).
            ai (bool): True if the game is played by AI, False if played manually.
        """
        self.row_pos = row_pos
        self.col_pos = col_pos
        self.row_n = row_n
        self.col_n = col_n
        self.ai = ai
        self.length_of_empty_cell = len(str(row_n * col_n))  # Calculate length of each cell
        self.empty_cell = self.length_of_empty_cell * "_"  # Placeholder for empty cell

        # Initialize the board as 2D list
        board = []
        for i in range(row_n + 1):
            row = []
            for j in range(col_n + 1):
                row.append(self.empty_cell)
            board.append(row)
        self.board = board

    def view_board(self):
        """
        Returns a formatted string representation of the game board.
        """
        # Prepare the top and bottom line
        top_bot_line = " " * len(str(self.col_n)) + "-" * ((self.length_of_empty_cell + 1) * self.col_n + 3) + '\n'
        # Prepare the board string starting with the top line
        board_string = top_bot_line
        for i in reversed(range(1, self.row_n + 1)):
            line = ""
            for j in range(1, self.col_n + 1):
                line += " " + self.board[i][j]
            left_number = ' ' * (len(str(self.row_n)) - len(str(i))) + str(i)
            board_string += left_number + "|" + line + " |\n"
        board_string += top_bot_line
        bot_numbers = " " * (len(str(self.col_n)) + 1)
        for i in range(1, self.col_n + 1):
            bot_numbers += (self.length_of_empty_cell - len(str(i)) + 1) * ' ' + str(i)
        board_string += bot_numbers
        return board_string

    def check_one_move(self, new_row_pos, new_col_pos):
        """
        Checks if a move to the specified position is possible.

        Args:
            new_row_pos (int): The row position to check.
            new_col_pos (int): The column position to check.

        Returns:
            int: 1 if the move is possible, 0 otherwise.
        """
        if 1 <= new_row_pos <= self.row_n and 1 <= new_col_pos <= self.col_n:
            string_set = set(self.board[new_row_pos][new_col_pos])
            if self.ai:
                for i in range(10):
                    if str(i) in string_set:
                        return 0
            if not self.ai:
                if 'X' in string_set or '*' in string_set:
                    return 0
            return 1
        return 0

    # Method to find all possible moves
    def possible_moves(self, rec, row_pos, col_pos):
        """
        Finds the possible moves from a given position on the board.

        Args:
            rec (int): The recursion depth.
            row_pos (int): The row position.
            col_pos (int): The column position.

        Returns:
            tuple: A tuple containing the number of possible moves, a list of possible moves, and a list of counts of moves possible from each position.
        """
        possible_moves_n = 0  # Count of possible moves from the current position
        possible_moves_table = []  # List to store the possible moves
        possible_moves_table_n = []  # List to store the count of moves possible from each position

        for row in [-2, -1, 1, 2]:
            for col in [-2, -1, 1, 2]:
                if row * row * col * col != 4:
                    continue

                poss = self.check_one_move(row_pos + row, col_pos + col)
                possible_moves_n += poss
                if poss == 1 and rec > 0:
                    possible_moves_table.append([row_pos + row, col_pos + col])
                    future_possible_moves_n, _, _ = self.possible_moves(rec - 1, row_pos + row, col_pos + col)
                    possible_moves_table_n.append(future_possible_moves_n)
        if rec > 0:
            sorted_pairs = sorted(zip(possible_moves_table_n, possible_moves_table), reverse=True)
            possible_moves_table_n = [pair[0] for pair in sorted_pairs]
            possible_moves_table = [pair[1] for pair in sorted_pairs]

        return possible_moves_n, possible_moves_table, possible_moves_table_n

    def input_position(self, sign, row_pos, col_pos):
        """
        Updates the game board with the specified sign at the given position.

        Args:
            sign (str): The sign to be placed on the board.
            row_pos (int): The row position.
            col_pos (int): The column position.
        """
        sign = str(sign)

        if sign == '_' or sign == ' ':
            self.board[row_pos][col_pos] = self.length_of_empty_cell * sign
        else:
            self.board[row_pos][col_pos] = (self.length_of_empty_cell - len(sign)) * ' ' + sign


def play_game(game):
    """
    Plays the game manually with the user making moves.

    Args:
        game (Game): The Game object.
    """
    # Initialization
    row_pos = game.row_pos
    col_pos = game.col_pos
    game.input_position('X', game.row_pos, game.col_pos)
    possible_moves_n, possible_moves_table, possible_moves_table_n = game.possible_moves(1, game.row_pos, game.col_pos)
    # Update the board with the number of possible moves from the possible moves table
    for i in range(possible_moves_n):
        game.input_position(possible_moves_table_n[i], possible_moves_table[i][0], possible_moves_table[i][1])
    print(game.view_board())

    old_possible_moves_table = possible_moves_table
    old_row_pos = row_pos
    old_col_pos = col_pos
    number_of_moves = 1

    while True:
        x = input("Enter your next move: ")
        new_pos = valid_position(x)
        row_pos = new_pos[1]
        col_pos = new_pos[0]

        # Check if the move is possible
        if game.check_one_move(row_pos, col_pos) == 0 or [row_pos, col_pos] not in old_possible_moves_table:
            print("Invalid move! ", end="")
            continue

        # Increase the number of moves
        number_of_moves += 1

        # Change the position of the old 'X' to '*'
        game.input_position('*', old_row_pos, old_col_pos)

        # Change old numbers to empty cells
        for pos in old_possible_moves_table:
            game.input_position("_", pos[0], pos[1])

        # Change position for the new 'X'
        game.input_position('X', row_pos, col_pos)

        possible_moves_n, possible_moves_table, possible_moves_table_n = game.possible_moves(1, row_pos, col_pos)

        # Update the board with the number of possible moves from the possible moves table
        for i in range(possible_moves_n):
            game.input_position(possible_moves_table_n[i], possible_moves_table[i][0], possible_moves_table[i][1])

        print(game.view_board())

        old_possible_moves_table = possible_moves_table
        old_row_pos = row_pos
        old_col_pos = col_pos

        if possible_moves_n == 0:
            if number_of_moves == game.row_n * game.col_n:
                print("What a great tour! Congratulations!")
                break
            else:
                print("No more possible moves!")
                print(f"Your knight visited {number_of_moves} squares!")
                break


def finish_ai(game, row_pos, col_pos, current_value):
    """
    Recursively tries to finish the game using AI.

    Args:
        game (Game): The Game object.
        row_pos (int): The current row position.
        col_pos (int): The current column position.
        current_value (int): The current value of the knight's position.

    Returns:
        bool: True if the game is finished, False otherwise.
    """

    if current_value == game.row_n * game.col_n:
        return True

    current_value += 1

    possible_moves_n, possible_moves_table, possible_moves_table_n = game.possible_moves(1, row_pos, col_pos)

    for i in range(possible_moves_n):
        row_pos = possible_moves_table[i][0]
        col_pos = possible_moves_table[i][1]
        game.input_position(current_value, row_pos, col_pos)

        if finish_ai(game, row_pos, col_pos, current_value):
            return True
        else:
            game.input_position(" ", row_pos, col_pos)

def play_ai(game):
    """
    Plays the game automatically using AI to find a solution.

    Args:
        game (Game): The Game object.
    """
    row_pos = game.row_pos
    col_pos = game.col_pos
    game.input_position(1, row_pos, col_pos)

    # Find the solution starting from the first position of the knight
    finish_ai(game, row_pos, col_pos, 1)

    print("Here's the solution!")

def main():
    """
    The main function to start the game.
    """
    row_position, col_position, row_n, col_n, ai = starting_messages()
    if not solution_exists(row_n, col_n):
        print("No solution exists!")
    else:
        game = Game(row_position, col_position, row_n, col_n, ai)
        if not game.ai:
            play_game(game)
        else:
            play_ai(game)
            print(game.view_board())


# Execute the main function when the script is run
if __name__ == "__main__":
    main()




