"""Monty Hall problem simulation.

This module provides:
- monty_hall(switch_doors): simulate a single 3-door game (doors 0..2).
- simulate(number_of_game): run many games and return win rates
  as a tuple (switch_win_rate, stay_win_rate).
"""

import random


def monty_hall(switch_doors: bool = True) -> bool:
    """Simulate one round of the Monty Hall game.

    Parameters:
        switch_doors: If True, switch after the host reveals a goat;
            if False, keep the original choice.

    Returns:
        True if the contestant wins the car with the final choice, else False.
    """
    car_door = random.randint(0, 2)

    user_guess = random.randint(0, 2)
    final_choice = user_guess

    # Host reveals a goat door (not the car, not user's choice)
    doors_reveal = [i for i in range(3) if i != user_guess and i != car_door]
    door_reveal = random.choice(doors_reveal)

    if switch_doors:
        # Switch to the remaining unopened door
        final_choice = [i for i in range(3) if i != user_guess and i != door_reveal][0]

    return final_choice == car_door


def simulate_monty_hall(number_of_games: int) -> tuple[float, float]:
    """Run multiple Monty Hall games and compute win rates.

    Parameters:
        number_of_game: Number of simulations to run.

    Returns:
        A tuple (switch_win_rate, stay_win_rate), each rounded to 2 decimals.
    """
    simulate_without_switching = sum(
        monty_hall(False) for _ in range(0, number_of_games)
    )
    simulate_with_switching = sum(monty_hall(True) for _ in range(0, number_of_games))
    return round(simulate_with_switching / number_of_games, 2), round(
        simulate_without_switching / number_of_games, 2
    )


if __name__ == "__main__":
    print(simulate_monty_hall(500))
