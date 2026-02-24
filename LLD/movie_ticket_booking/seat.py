"""Seat entity for a screen in the booking system."""


class Seat:
    """A single seat in a screen.

    Attributes:
        id: Unique seat identifier (e.g. "A1").
        row: Row label (e.g. "A", "B", "C").
        column: Column number (1, 2, 3, ...).
        booked: Whether the seat is currently booked.
    """

    def __init__(
        self, id: str, row: str, column: int, booked: bool = False
    ) -> None:
        """Initialize a seat.

        Args:
            id: Unique seat identifier.
            row: Row label (A–Z).
            column: Column number (1–20 typically).
            booked: Whether the seat is already booked. Defaults to False.
        """
        self.id: str = id
        self.row: str = row
        self.column: int = column
        self.booked: bool = booked

    def get_id(self) -> str:
        """Return the seat's unique identifier."""
        return self.id

    def get_row(self) -> str:
        """Return the seat's row label."""
        return self.row

    def get_column(self) -> int:
        """Return the seat's column number."""
        return self.column

    def is_booked(self) -> bool:
        """Return True if the seat is booked, False otherwise."""
        return self.booked

    def book(self) -> None:
        """Mark the seat as booked."""
        self.booked = True

    def cancel(self) -> None:
        """Mark the seat as not booked."""
        self.booked = False