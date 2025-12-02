import random


class TicTacToe:
    """Tic Tac Toe game implementation."""

    def __init__(self):
        # Initialize empty 3x3 board
        self.board = [[" " for _ in range(3)] for _ in range(3)]
        self.player = self.get_random_first_player()

    def get_random_first_player(self):
        # Randomly choose starting player
        return "X" if random.randint(0, 1) == 0 else "O"

    def has_player_won(self):
        # check rows
        for row in self.board:
            if all(cell == self.player for cell in row):
                return True
        # check columns
        for col_index in range(3):
            if all(
                self.board[row_index][col_index] == self.player
                for row_index in range(3)
            ):
                return True
        # check main diagonal
        if all(self.board[i][i] == self.player for i in range(3)):
            return True

        # check anti-diagonal
        if all(self.board[i][2 - i] == self.player for i in range(3)):
            return True

        return False

    def board_is_full(self):
        # Check if all cells are occupied
        return all(cell != " " for row in self.board for cell in row)

    def swap_player(self):
        # Alternate between X and O
        if self.player == "X":
            self.player = "O"
        else:
            self.player = "X"

    def mark_a_cell(self, x: int, y: int):
        # Mark cell with current player's symbol
        if self.board[x][y] == " ":
            self.board[x][y] = self.player
            self.show_board()
        else:
            raise Exception("The cell is already marked!")

    def show_board(self):
        print("\n")
        for row in self.board:
            row_str = "|"
            for colum in row:
                row_str += colum + "|"
            print(row_str, "\n")
        print("\n")

    def play(self):
        self.show_board()
        # Main game loop
        while True:
            try:
                row, col = self.get_user_move()

                self.mark_a_cell(row, col)

                # Check for win
                if self.has_player_won():
                    print(f"Player {self.player} is the winner!")
                    break

                # Check for draw
                if self.board_is_full():
                    print("It's a draw")
                    break

                self.swap_player()

            except Exception as e:
                print(f"{e}")
                print("Invalid move, Try again")
                continue

    def get_user_move(self):
        """Get and validate user input for cell coordinates."""
        while True:
            try:
                user_input = input(
                    f"Player {self.player}, Which cell do you want to mark? Tell as x, y: "
                ).strip()
                
                # Check if input is empty
                if not user_input:
                    print("Error: Please enter two numbers separated by a comma.")
                    continue
                
                # Split input and validate we got exactly 2 values
                parts = user_input.split(",")
                if len(parts) != 2:
                    print(f"Error: Expected 2 values separated by a comma, got {len(parts)}. Example: 1,2")
                    continue
                
                # Extract and strip whitespace from coordinates
                x_str, y_str = parts[0].strip(), parts[1].strip()
                
                # Validate that both parts are numeric
                try:
                    row = int(x_str)
                    col = int(y_str)
                except ValueError:
                    print(f"Error: '{x_str}' and '{y_str}' must be numbers. Example: 0,1 or 1,2")
                    continue
                
                # Validate row is within bounds (0-2)
                if row < 0 or row > 2:
                    print(f"Error: Row must be between 0 and 2, got {row}")
                    continue
                
                # Validate column is within bounds (0-2)
                if col < 0 or col > 2:
                    print(f"Error: Column must be between 0 and 2, got {col}")
                    continue
                
                # Check if cell is already occupied
                if self.board[row][col] != " ":
                    print(f"Error: Cell ({row}, {col}) is already marked with '{self.board[row][col]}'. Choose another cell.")
                    continue
                
                print(f"You entered: {row}, {col}")
                return row, col
                
            except KeyboardInterrupt:
                print("\n\nGame interrupted by user. Exiting...")
                raise  # Re-raise to allow the calling code to handle exit
            except EOFError:
                print("\n\nEnd of input reached. Exiting...")
                raise  # Re-raise to allow the calling code to handle exit


if __name__ == "__main__":
    # Start the game
    ticTacToe = TicTacToe()
    ticTacToe.play()
