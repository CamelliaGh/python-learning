"""User entity and mock user registry."""

from __future__ import annotations

from typing import Dict, List


class User:
    """A user who can make reservations.

    Attributes:
        id: Unique identifier for the user.
        name: Display name.
        email: Email address.
        reservations: List of reservations made by this user.
    """

    def __init__(self, id: str, name: str, email: str) -> None:
        """Initialize a user.

        Args:
            id: Unique identifier.
            name: Display name.
            email: Email address.
        """
        self.id: str = id
        self.name: str = name
        self.email: str = email
        self.reservations: List["Reservation"] = []

    def get_name(self) -> str:
        """Return the user's display name."""
        return self.name

    def get_reservations(self) -> List["Reservation"]:
        """Return all reservations made by this user."""
        return self.reservations


# Mock user data for demo purposes.
users: Dict[str, User] = {
    "1": User("1", "John Doe", "john.doe@example.com"),
    "2": User("2", "Jane Doe", "jane.doe@example.com"),
    "3": User("3", "Jim Doe", "jim.doe@example.com"),
}