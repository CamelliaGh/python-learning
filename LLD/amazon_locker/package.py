from enum import Enum


class Size(Enum):
    """Package or compartment size (ordered: SMALL < MEDIUM < LARGE)."""

    SMALL = 1
    MEDIUM = 2
    LARGE = 3

    def __ge__(self, other: 'Size') -> bool:
        return self.value >= other.value

    def __le__(self, other: 'Size') -> bool:
        return self.value <= other.value

    def __gt__(self, other: 'Size') -> bool:
        return self.value > other.value

    def __lt__(self, other: 'Size') -> bool:
        return self.value < other.value


class Package:
    """A package with an id and size, to be stored in a locker compartment."""

    def __init__(self, id: int, size: Size):
        """Create a package with the given id and size."""
        self._id = id
        self._size = size

    def get_id(self):
        """Return the package id."""
        return self._id

    def get_size(self):
        """Return the package size."""
        return self._size

    def __str__(self):
        return f"Package(id={self._id}, size={self._size})"