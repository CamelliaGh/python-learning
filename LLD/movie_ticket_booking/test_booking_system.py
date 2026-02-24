"""Simple tests for the booking system using assert statements."""

from reservation import ReservationStatus

from booking_system import BookingSystem
from movie import Movie
from screen import Screen
from seat import Seat
from show_time import ShowTime
from theatre import Theatre


def _make_test_system():
    """Build a minimal theatre + booking system for tests (uses global users '1')."""
    s1 = Seat("A1", "A", 1)
    s2 = Seat("A2", "A", 2)
    screen = Screen("Screen 1", seats=[s1, s2])
    movie = Movie("Test Movie", "m1")
    showtime = ShowTime("st1", movie, screen, "2026-01-01", "10:00")
    theater = Theatre("T1", screens=[screen], show_times=[showtime])
    return BookingSystem([theater]), showtime, [s1, s2]


def test_get_movies():
    system, showtime, _ = _make_test_system()
    theater = system.theaters[0]
    movies = system.get_movies(theater, "2026-01-01")
    assert len(movies) == 1
    assert movies[0].title == "Test Movie"
    assert movies[0].id == "m1"


def test_get_seats():
    system, showtime, seats = _make_test_system()
    result = system.get_seats(showtime)
    assert len(result) == 2
    ids = {s.id for s in result}
    assert ids == {"A1", "A2"}


def test_book_and_reservation():
    system, showtime, seats = _make_test_system()
    s1, s2 = seats
    reservation = system.book(showtime, [s1, s2], "1")
    assert reservation is not None
    assert reservation.id in system.reservations
    assert reservation.status == ReservationStatus.CONFIRMED
    assert s1.is_booked() and s2.is_booked()
    user_reservations = system.get_reservations("1")
    assert reservation in user_reservations


def test_cancel():
    system, showtime, seats = _make_test_system()
    s1, s2 = seats
    reservation = system.book(showtime, [s1, s2], "1")
    rid = reservation.id
    cancelled = system.cancel(rid)
    assert cancelled.status == ReservationStatus.CANCELLED
    assert not s1.is_booked() and not s2.is_booked()
    assert rid not in system.reservations
    assert reservation not in system.get_reservations("1")


def test_book_already_booked_raises():
    system, showtime, seats = _make_test_system()
    s1, s2 = seats
    system.book(showtime, [s1], "1")
    try:
        system.book(showtime, [s1], "2")
        assert False, "expected ValueError"
    except ValueError as e:
        assert "already booked" in str(e).lower()


def test_cancel_nonexistent_raises():
    system, _, _ = _make_test_system()
    try:
        system.cancel("nonexistent-id")
        assert False, "expected ValueError"
    except ValueError as e:
        assert "not found" in str(e).lower()


if __name__ == "__main__":
    test_get_movies()
    test_get_seats()
    test_book_and_reservation()
    test_cancel()
    test_book_already_booked_raises()
    test_cancel_nonexistent_raises()
    print("All tests passed.")
