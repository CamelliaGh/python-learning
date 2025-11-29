"""Utilities for working with happy numbers.

A happy number is an integer that eventually reaches 1 when iteratively
replacing the number by the sum of the squares of its digits. Numbers that
enter a loop and never reach 1 are called unhappy.
"""


def is_happy_number(n: int):
    """Return whether the integer n is a happy number.

    Args:
        n: A positive integer to test.

    Returns:
        True if n is a happy number, otherwise False.
    """
    seen_numbers = set()
    while (n != 1 and n not in seen_numbers):
        seen_numbers.add(n)
        n = sum([int(i) ** 2 for i in str(n)])

    return n == 1


if __name__ == '__main__':
    assert is_happy_number(7) is True
    assert is_happy_number(44) is True
    assert is_happy_number(45) is False
    assert is_happy_number(25) is False
