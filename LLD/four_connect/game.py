"""Four Connect game: two players take turns dropping discs into columns."""

import random

from board import Board
from player import Player


class Game:
    """Orchestrates a single Four Connect match: turns, input, and game-over handling."""

    def __init__(self, rows, columns, player1, player2):
        """Initialize a new game.

        Args:
            rows: Number of board rows.
            columns: Number of board columns.
            player1: First player (Player instance).
            player2: Second player (Player instance).
        """
        self._board = Board(rows, columns)
        self._player1 = player1
        self._player2 = player2
        self._current_player = player1 if random.randint(0, 1) == 0 else player2

    def make_move(self, player: Player):
        """Prompt for a column, then place the player's disc on the board."""
        column = self.get_column(player)
        row = self.get_row(column)
        self._board.make_move(row, column, player.get_disc_color())

    def switch_player(self):
        """Set the current player to the other player."""
        self._current_player = self._player1 if self._current_player == self._player2 else self._player2

    def get_column(self, player: Player):
        """Read a valid column from the user for the given player.

        Returns:
            The chosen column index.

        Raises:
            ValueError: If input is invalid (non-numeric, etc.) or the move is invalid (out of range, column full).
        """
        max_col = self._board.max_column_index
        user_input = input(f"{player.get_name()}'s turn: enter a column between 0 and {max_col}: ").strip()
        column = self._parse_column_input(user_input)
        self._validate_column_move(column)
        return column

    def _parse_column_input(self, user_input: str) -> int:
        """Parse user input into a column index. Input validation only (format/type).

        Returns:
            The column index as an integer.

        Raises:
            ValueError: If the input is not a number.
        """
        try:
            return int(user_input)
        except ValueError:
            raise ValueError("Please enter a number.")

    def _validate_column_move(self, column: int) -> None:
        """Check that the column is a valid move according to game rules.

        Raises:
            ValueError: If the column is out of range or full.
        """
        max_col = self._board.max_column_index
        if not self._board.is_valid_move(column):
            raise ValueError(f"Invalid column. Enter a number between 0 and {max_col}.")
        if self._board.is_column_full(column):
            raise ValueError("That column is full. Choose another.")

    def get_row(self, column):
        """Return the row index where a disc would land in the given column."""
        return self._board.get_row(column)

    def play(self):
        """Run the game loop until a win, draw, or unrecovered error."""
        while True:
            try:
                self.make_move(self._current_player)
                self._board.print_board()
                if self._board.check_win(self._current_player.get_disc_color()):
                    print(f"{self._current_player.get_name()} wins!")
                    break
                if self._board.check_draw():
                    print("It's a draw!")
                    break
                self.switch_player()
            except ValueError as e:
                print(e)

if __name__ == "__main__":
    game = Game(6, 7, Player("Player Y", "Yellow"), Player("Player R", "Red"))
    game.play()