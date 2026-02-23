class Board:
    """Game board for Four Connect: grid state and win/draw checks."""

    def __init__(self, rows, columns):
        """Initialize an empty board.

        Args:
            rows: Number of rows.
            columns: Number of columns.
        """
        self._rows = rows
        self._columns = columns
        self._board = [[' ' for _ in range(columns)] for _ in range(rows)]

    def print_board(self):
        """Print the current board state to stdout."""
        for row in self._board:
            print('|'.join(row))
            print('-' * (self._columns * 2 - 1))

    @property
    def rows(self):
        """Number of rows on the board."""
        return self._rows

    @property
    def columns(self):
        """Number of columns on the board."""
        return self._columns

    @property
    def max_column_index(self):
        """Largest valid column index (0-based)."""
        return self._columns - 1

    def is_valid_move(self, col):
        """Return True if a disc can be dropped in the given column."""
        return 0 <= col < self._columns

    def is_column_full(self, col):
        """Return True if the given column has no empty cell."""
        return self._board[0][col] != ' '

    def get_row(self, column):
        """Return the lowest empty row index for the given column.

        Raises:
            ValueError: If the column is full.
        """
        for row in range(0, self._rows):
            if self._board[row][column] == ' ':
                return row
        raise ValueError("Column is full. Try again.")

    def make_move(self, row, column, disc_color):
        """Place a disc of the given color at (row, column)."""
        self._board[row][column] = disc_color

    def check_draw(self):
        """Return True if the board is full with no winner."""
        return all(cell != ' ' for row in self._board for cell in row)

    def check_win(self, disc_color):
        """Return True if the given disc color has four in a row (any direction)."""
        return self.check_horizontal_win(disc_color) or self.check_vertical_win(disc_color) or self.check_diagonal_win(disc_color)

    def check_horizontal_win(self, disc_color):
        """Return True if any row has four consecutive discs of the given color."""
        for row in self._board:
            for i in range(len(row) - 3):
                if row[i] == disc_color and row[i+1] == disc_color and row[i+2] == disc_color and row[i+3] == disc_color:
                    return True
        return False

    def check_vertical_win(self, disc_color):
        """Return True if any column has four consecutive discs of the given color."""
        for col in range(len(self._board[0])):
            for i in range(len(self._board) - 3):
                if self._board[i][col] == disc_color and self._board[i+1][col] == disc_color and self._board[i+2][col] == disc_color and self._board[i+3][col] == disc_color:
                    return True
        return False

    def check_diagonal_win(self, disc_color):
        """Return True if any diagonal has four consecutive discs of the given color."""
        # Top-left to bottom-right (direction 1, 1)
        for i in range(len(self._board) - 3):
            for j in range(len(self._board[0]) - 3):
                if self._board[i][j] == disc_color and self._board[i+1][j+1] == disc_color and self._board[i+2][j+2] == disc_color and self._board[i+3][j+3] == disc_color:
                    return True
        # Top-right to bottom-left (direction 1, -1)
        for i in range(len(self._board) - 3):
            for j in range(3, len(self._board[0])):
                if self._board[i][j] == disc_color and self._board[i+1][j-1] == disc_color and self._board[i+2][j-2] == disc_color and self._board[i+3][j-3] == disc_color:
                    return True
        return False