"""Show time entity: a movie screening at a screen on a date and time."""

from movie import Movie
from screen import Screen


class ShowTime:
    """A scheduled screening of a movie at a screen.

    Attributes:
        id: Unique identifier for the show time.
        movie: The movie being shown.
        screen: The screen where it is shown.
        date: Date string (e.g. "YYYY-MM-DD").
        time_range: Time string (e.g. "10:00").
    """

    def __init__(
        self,
        id: str,
        movie: Movie,
        screen: Screen,
        date: str,
        time_range: str,
    ) -> None:
        """Initialize a show time.

        Args:
            id: Unique identifier for the show time.
            movie: The movie to show.
            screen: The screen to use.
            date: Date in YYYY-MM-DD format.
            time_range: Start time string.
        """
        self.id: str = id
        self.movie: Movie = movie
        self.screen: Screen = screen
        self.date: str = date
        self.time_range: str = time_range

    def get_movie(self) -> Movie:
        """Return the movie for this show time."""
        return self.movie

    def get_screen(self) -> Screen:
        """Return the screen for this show time."""
        return self.screen

    def is_available(self) -> bool:
        """Return True if this show time is still available for booking."""
        return True