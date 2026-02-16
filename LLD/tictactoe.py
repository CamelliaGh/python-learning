"""
Low-Level Design: Tic-Tac-Toe Game

This module implements a console-based Tic-Tac-Toe game with proper OOP design.

Entities:
    - Game: Orchestrates gameplay and manages game state
    - Board: Manages the 3x3 game board
    - Player: Represents a player with a symbol (X or O)
    - GameState: Enum for game states (WIN, DRAW, IN_PROGRESS)

Relations:
    - Game has one Board
    - Game has two Players
    - Game tracks current_player

States:
    Game:
        - current_player: Currently active player
        - player_1: First player (X)
        - player_2: Second player (O)
        - board: Game board instance
        
Behaviors:
    Game:
        - make_a_move: Process a player's move
        - switch_player: Toggle between players
        - get_game_state: Check win/draw/in-progress
        - play: Main game loop
"""

import random
from enum import Enum


class GameState(Enum):
    """Enumeration of possible game states."""
    WIN = "win"
    DRAW = "draw"
    IN_PROGRESS = "in_progress"


class Player:
    """
    Represents a Tic-Tac-Toe player.
    
    Attributes:
        symbol (str): Player's mark on the board ('X' or 'O')
        name (str): Player's display name
    """
    
    def __init__(self, symbol: str, name: str = None):
        """
        Initialize a player with a symbol and optional name.
        
        Args:
            symbol (str): The player's symbol ('X' or 'O')
            name (str, optional): Player's name. Defaults to "Player {symbol}"
        """
        self.symbol = symbol
        self.name = name or f"Player {symbol}"

    def __str__(self):
        """Return the player's name as string representation."""
        return self.name


class Board:
    """
    Represents the 3x3 Tic-Tac-Toe game board.
    
    Attributes:
        board (list[list[str]]): 2D array representing the game board
    """
    
    def __init__(self):
        """Initialize an empty 3x3 board with spaces."""
        self.board = [[" " for _ in range(3)] for _ in range(3)]

    def mark(self, x: int, y: int, symbol: str) -> None:
        """
        Mark a cell on the board with a player's symbol.
        
        Args:
            x (int): Row index (0-2)
            y (int): Column index (0-2)
            symbol (str): Player's symbol to mark
            
        Raises:
            ValueError: If coordinates are out of range or cell is occupied
        """
        if x < 0 or x > 2 or y < 0 or y > 2:
            raise ValueError("Out of range")

        if self.board[x][y].strip():
            raise ValueError("The cell is not empty")
        
        self.board[x][y] = symbol
        print(self)

    def __str__(self):
        """
        Return a string representation of the board.
        
        Returns:
            str: Formatted board with cell separators
        """
        rp = ""
        rp += f"{' | '.join(self.board[0])}\n"
        rp += "----------\n"
        rp += f"{' | '.join(self.board[1])}\n"
        rp += "----------\n"
        rp += f"{' | '.join(self.board[2])}\n"
        return rp

    def is_full(self) -> bool:
        """
        Check if the board is completely filled.
        
        Returns:
            bool: True if all cells are occupied, False otherwise
        """
        return all(cell != ' ' for row in self.board for cell in row)


class Game:
    """
    Manages the Tic-Tac-Toe game logic and flow.
    
    Attributes:
        board (Board): The game board
        player_1 (Player): First player (X)
        player_2 (Player): Second player (O)
        current_player (Player): Currently active player
    """
    
    def __init__(self):
        """Initialize a new game with empty board and two players."""
        self.board = Board()
        self.player_1 = Player("X")
        self.player_2 = Player("O")
        self.current_player = None

    def get_random_player(self) -> Player:
        """
        Randomly select which player goes first.
        
        Returns:
            Player: Randomly selected player (player_1 or player_2)
        """
        return self.player_1 if random.randint(0, 1) == 0 else self.player_2

    def make_a_move(self, x: int, y: int) -> None:
        """
        Process a player's move on the board.
        
        Note: Currently has a bug - parameters x, y are ignored and 
        get_cell_x_y() is called instead within the loop.
        
        Args:
            x (int): Row coordinate (not currently used)
            y (int): Column coordinate (not currently used)
            
        Raises:
            ValueError: If move is invalid (handled internally)
        """
        while True:
            try:
                x, y = self.get_cell_x_y()
                print(f"{self.current_player.symbol} marked {x},{y}")
                self.board.mark(x, y, self.current_player.symbol)
                break
            except ValueError as e:
                print(f"Invalid input: {e}")

    def get_cell_x_y(self) -> tuple[int, int]:
        """
        Get cell coordinates from user input.
        
        Returns:
            tuple[int, int]: Validated (x, y) coordinates
            
        Raises:
            ValueError: If input format is invalid or conversion fails
        """
        xy = input(
            f" {self.current_player} two numbers between 0 to 2 "
            f"indicating the cell address in the format of x, y:"
        )
        parts = xy.replace(',', ' ').split()
        if len(parts) != 2:
            raise ValueError("Enter exactly 2 numbers")
        
        x, y = int(parts[0]), int(parts[1])
        return x, y

    def switch_player(self) -> None:
        """Switch the current player to the other player."""
        if self.current_player == self.player_1:
            self.current_player = self.player_2
        else:
            self.current_player = self.player_1

    def get_game_state(self) -> GameState:
        """
        Determine the current state of the game.
        
        Checks for:
        - Row wins (3 in a row horizontally)
        - Column wins (3 in a row vertically)
        - Diagonal wins (both diagonals)
        - Draw (board full with no winner)
        - In progress (game continues)
        
        Returns:
            GameState: Current state (WIN, DRAW, or IN_PROGRESS)
        """
        # Check rows and columns
        for i in range(3):
            # Check column
            if (
                self.board.board[0][i]
                == self.board.board[1][i]
                == self.board.board[2][i]
                and self.board.board[0][i] == self.current_player.symbol
            ):
                return GameState.WIN
            
            # Check row
            if (
                self.board.board[i][0]
                == self.board.board[i][1]
                == self.board.board[i][2]
                and self.board.board[i][0] == self.current_player.symbol
            ):
                return GameState.WIN

        # Check diagonal (top-left to bottom-right)
        if (
            self.board.board[0][0] == self.board.board[1][1] == self.board.board[2][2]
            and self.board.board[0][0] == self.current_player.symbol
        ):
            return GameState.WIN

        # Check diagonal (top-right to bottom-left)
        if (
            self.board.board[0][2] == self.board.board[1][1] == self.board.board[2][0]
            and self.board.board[1][1] == self.current_player.symbol
        ):
            return GameState.WIN

        # Check for draw
        if self.board.is_full():
            return GameState.DRAW

        return GameState.IN_PROGRESS

    def play(self) -> None:
        """
        Main game loop - runs until game ends in win or draw.
        
        Randomly selects starting player, then alternates turns until
        the game reaches a terminal state (WIN or DRAW).
        """
        self.current_player = self.get_random_player()
        while True:
            x, y = self.get_cell_x_y()
            self.make_a_move(x, y)
            state = self.get_game_state()
            
            if state == GameState.WIN:
                print(f"{self.current_player} is the winner")
                break
            elif state == GameState.DRAW:
                print("It's a draw!")
                break

            self.switch_player()


if __name__ == "__main__":
    game = Game()
    game.play()