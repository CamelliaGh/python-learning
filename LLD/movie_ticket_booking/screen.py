"""Screen entity: a room with seats for a show."""

from __future__ import annotations

import threading
from typing import Dict, List, Optional

from seat import Seat


class Screen:
    """A screen (auditorium) containing a set of seats.

    Attributes:
        id: Unique identifier for the screen.
        seats: List of seats in this screen.
    """

    def __init__(self, id: str, seats: Optional[List[Seat]] = None) -> None:
        """Initialize a screen.

        Args:
            id: Unique identifier for the screen.
            seats: Optional list of seats. Defaults to empty list.
        """
        self.id: str = id
        self.seats: List[Seat] = list(seats) if seats else []
        self._seats_by_id: Dict[str, Seat] = {s.id: s for s in self.seats}
        self._lock: threading.Lock = threading.Lock()

    def get_seats(self) -> List[Seat]:
        """Return all seats in this screen."""
        return self.seats

    def get_seat(self, seat_id: str) -> Seat:
        """Return the seat with the given id. Raises KeyError if not found."""
        return self._seats_by_id[seat_id]

    def book_seat(self, seat_id: str) -> None:
        """Mark the seat with the given id as booked (thread-safe)."""
        with self._lock:
            self._seats_by_id[seat_id].book()

    def cancel_seat(self, seat_id: str) -> None:
        """Mark the seat with the given id as not booked (thread-safe)."""
        with self._lock:
            self._seats_by_id[seat_id].cancel()
