"""Theatre entity: a venue with screens and show times."""

from typing import List, Optional

from screen import Screen
from show_time import ShowTime


class Theatre:
    """A theatre venue containing multiple screens and show times.

    Attributes:
        id: Unique identifier for the theatre.
        screens: List of screens in this theatre.
        show_times: List of show times (any screen, any date).
    """

    def __init__(
        self,
        id: str,
        screens: Optional[List[Screen]] = None,
        show_times: Optional[List[ShowTime]] = None,
    ) -> None:
        """Initialize a theatre.

        Args:
            id: Unique identifier for the theatre.
            screens: Optional list of screens. Defaults to empty list.
            show_times: Optional list of show times. Defaults to empty list.
        """
        self.id: str = id
        self.screens: List[Screen] = screens if screens is not None else []
        self.show_times: List[ShowTime] = show_times if show_times is not None else []

    def get_screens(self) -> List[Screen]:
        """Return all screens in this theatre."""
        return self.screens

    def get_show_times(self, date: Optional[str] = None) -> List[ShowTime]:
        """Return show times, optionally filtered by date (YYYY-MM-DD)."""
        if date is None:
            return self.show_times
        return [st for st in self.show_times if st.date == date]