
"""Rock Paper Scissors command-line game.

This module defines the `Game` class for playing Rock–Paper–Scissors against
the computer in the terminal.

Gameplay:
- Enter 'rock', 'paper', or 'scissors' when prompted.
- Enter 'q' to quit the game.
- The computer's move is chosen with `random.choice`.

The game validates user input, prints the computer's choice, and announces the
round result.

Example:
    >>> game = Game()
    >>> game.play()
"""

import random
from typing import List


class Game:
    GAME_OPTIONS: List[str] = ['rock', 'paper', 'scissors']

    def __init__(self):
        """Initialize a new game instance."""
        pass

    def play(self):
        """Run the main game loop until the user quits.

        Prompts for the user's choice, generates the computer's choice, and
        prints the outcome of each round.
        """
        while True:
            user_choice = self.get_user_choice()
            
            if user_choice == 'q':
                print("Game is over!")
                break
            
            computer_choice = self.get_computer_choice()
            self.choose_winner(user_choice, computer_choice)

    def get_user_choice(self):
        """Prompt for and validate the user's move.

        Returns:
            str: 'q' if the user quits; otherwise, a valid choice in
            {'rock', 'paper', 'scissors'}.
        """
        inp = input(
            "Enter your choice: ")
        
        if inp == 'q':
            return inp
        
        if inp.lower() not in self.GAME_OPTIONS:
            print("Invalid input")
            return self.get_user_choice()
            
        return inp

    def get_computer_choice(self) -> str:
        """Randomly select the computer's move and print it.

        Returns:
            str: The computer's choice: 'rock', 'paper', or 'scissors'.
        """
        random_choice = random.choice(self.GAME_OPTIONS)
        print(f"Computer choice is {random_choice}")
        return random_choice

    def choose_winner(self, user_choice: str, computer_choice: str) -> None:
        """Determine and print the winner for a single round.

        Args:
            user_choice (str): The user's selection.
            computer_choice (str): The computer's selection.
        """
        win_combinations = {('rock', 'scissors'),
                            ('paper', 'rock'), ('scissors', 'paper')}

        if user_choice == computer_choice:
            print("It's a tie!")
        elif (user_choice, computer_choice) in win_combinations:
            print("User is winner")
        else:
            print("Computer won!")


if __name__ == '__main__':
    game = Game()
    game.play()
    print(game.play.__doc__)