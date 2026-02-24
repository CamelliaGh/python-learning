"""Reservation entity and status enum."""

from enum import Enum
from typing import List

from seat import Seat
from show_time import ShowTime
from user import User


class ReservationStatus(Enum):
    """Status of a reservation."""

    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"


class Reservation:
    """A user's reservation for seats at a show time.

    Attributes:
        id: Unique reservation identifier.
        showtime: The show time being reserved.
        seats: List of seats reserved.
        user: The user who made the reservation.
        status: Current status (PENDING, CONFIRMED, CANCELLED).
    """

    def __init__(
        self,
        id: str,
        showtime: ShowTime,
        seats: List[Seat],
        user: User,
    ) -> None:
        """Initialize a reservation (starts as PENDING).

        Args:
            id: Unique reservation identifier.
            showtime: The show time to reserve.
            seats: Seats to reserve.
            user: The user making the reservation.
        """
        self.id: str = id
        self.showtime: ShowTime = showtime
        self.seats: List[Seat] = seats
        self.user: User = user
        self.status: ReservationStatus = ReservationStatus.PENDING

    def get_showtime(self) -> ShowTime:
        """Return the show time for this reservation."""
        return self.showtime

    def book(self) -> None:
        """Confirm the reservation: mark all seats as booked and set status to CONFIRMED."""
        for seat in self.seats:
            seat.book()
        self.status = ReservationStatus.CONFIRMED

    def cancel(self) -> None:
        """Cancel the reservation: release seats and set status to CANCELLED."""
        for seat in self.seats:
            seat.cancel()
        self.status = ReservationStatus.CANCELLED