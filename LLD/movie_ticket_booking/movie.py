"""Movie entity for the booking system."""


class Movie:
    """A movie that can be shown at a theatre.

    Attributes:
        title: Display name of the movie.
        id: Unique identifier for the movie.
    """

    def __init__(self, title: str, movie_id: str) -> None:
        """Initialize a movie.

        Args:
            title: Display name of the movie.
            movie_id: Unique identifier for the movie.
        """
        self.title: str = title
        self.id: str = movie_id