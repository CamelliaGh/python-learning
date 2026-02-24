"""Movie ticket booking system: theatres, show times, reservations."""

import uuid
from datetime import datetime
from typing import Dict, List, Optional
import threading

from movie import Movie
from reservation import Reservation
from screen import Screen
from seat import Seat
from show_time import ShowTime
from theatre import Theatre
from user import User, users


class BookingSystem:
    """Central booking system managing theatres and reservations.

    Attributes:
        theaters: List of theatres in the system.
        reservations: Map of reservation id to Reservation.
    """

    def __init__(self, theaters: List[Theatre]) -> None:
        """Initialize the booking system with the given theatres.

        Args:
            theaters: List of theatres to manage.
        """
        self.theaters: List[Theatre] = theaters
        self.reservations: Dict[str, Reservation] = {}
        self._lock = threading.Lock()

    def get_showtimes_at_theater(self, theater: Theatre) -> List[ShowTime]:
        """Return all show times at the given theatre."""
        return theater.get_show_times()

    def book(self, showtime: ShowTime, seats: List[Seat], user_id: str) -> Reservation:
        """Book the given seats for the show time for the user.

        Args:
            showtime: The show time to book.
            seats: Seats to book (must belong to the show's screen).
            user_id: Id of the user making the booking.

        Returns:
            The created and confirmed reservation.

        Raises:
            ValueError: If any seat is already booked, any seat is not on the
                show's screen, or the show time is not available.
        """
        with self._lock:
            if any(seat.is_booked() for seat in seats):
                raise ValueError("One or more seats are already booked")
            screen_seats = set(showtime.get_screen().get_seats())
            if not all(seat in screen_seats for seat in seats):
                raise ValueError("One or more seats are not in this show's screen")
            if not showtime.is_available():
                raise ValueError("Showtime is not available")
            reservation_id = str(uuid.uuid4())
            user = self.get_user(user_id)
            reservation = Reservation(reservation_id, showtime, seats, user)
            reservation.book()
            self.reservations[reservation_id] = reservation
            user.reservations.append(reservation)
            return reservation

    def cancel(self, reservation_id: str) -> Reservation:
        """Cancel the reservation with the given id.

        Returns:
            The cancelled reservation.

        Raises:
            ValueError: If no reservation exists with that id.
        """
        with self._lock:    
            reservation = self.reservations.get(reservation_id)
            if not reservation:
                raise ValueError("Reservation not found")
            reservation.cancel()
            del self.reservations[reservation_id]
            self.get_user(reservation.user.id).reservations.remove(reservation)
            return reservation  

    def get_reservations(self, user_id: str) -> List[Reservation]:
        """Return a snapshot of all reservations for the given user (thread-safe)."""
        with self._lock:
            return list(self.get_user(user_id).get_reservations())

    def get_movies(
        self,
        theater: Optional[Theatre] = None,
        date: Optional[str] = None,
    ) -> List[Movie]:
        """Return movies showing at a theatre on a date.

        Args:
            theater: Theatre to query; defaults to the first theatre.
            date: Date in YYYY-MM-DD; defaults to today.

        Returns:
            List of movies at that theatre on that date.
        """
        if theater is None:
            theater = self.theaters[0]
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")
        return [st.get_movie() for st in theater.get_show_times(date)]

    def get_user(self, user_id: str) -> User:
        """Return the user with the given id. Raises KeyError if not found."""
        return users[user_id]

    def get_seats(self, showtime: ShowTime) -> List[Seat]:
        """Return all seats for the given show time's screen."""
        return showtime.get_screen().get_seats()


if __name__ == "__main__":
    # create a few theaters, screens, seats, showtimes, movies

    seat1 = Seat("A1", "A", 1)
    seat2 = Seat("A2", "A", 2)
    seat3 = Seat("B1", "B", 1)
    seat4 = Seat("B2", "B", 2)
    seat5 = Seat("C1", "C", 1)
    seat6 = Seat("C2", "C", 2)
    seat7 = Seat("D1", "D", 1)
    seat8 = Seat("D2", "D", 2)

    screen1 = Screen("Screen 1", seats=[seat1, seat2])
    screen2 = Screen("Screen 2", seats=[seat3, seat4])
    screen3 = Screen("Screen 3", seats=[seat5, seat6])
    screen4 = Screen("Screen 4", seats=[seat7, seat8])

    movie1 = Movie("Movie 1", "1")
    movie2 = Movie("Movie 2", "2")
    movie3 = Movie("Movie 3", "3")
    movie4 = Movie("Movie 4", "4")

    showtime1 = ShowTime("1", movie1, screen1, "2026-01-01", "10:00")
    showtime2 = ShowTime("2", movie2, screen2, "2026-01-01", "10:00")
    showtime3 = ShowTime("3", movie3, screen3, "2026-01-01", "10:00")
    showtime4 = ShowTime("4", movie4, screen4, "2026-01-01", "10:00")

    theater1 = Theatre(
        "Theater1", screens=[screen1, screen2], show_times=[showtime1, showtime2]
    )
    theater2 = Theatre(
        "Theater2", screens=[screen3, screen4], show_times=[showtime3, showtime4]
    )


    booking_system = BookingSystem([theater1, theater2])
    print(booking_system.get_movies())
    print(booking_system.get_movies(theater1, "2026-01-01"))
    print(booking_system.get_movies(theater2, "2026-01-01"))
    print(booking_system.get_seats(showtime1))
    print(booking_system.get_seats(showtime2))
    print(booking_system.get_seats(showtime3))
    print(booking_system.get_seats(showtime4))

    reservation = booking_system.book(showtime1, [seat1, seat2], "1")
    print(reservation)
   
    print(booking_system.cancel(reservation.id))
