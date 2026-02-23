from package import Package, Size


class Compartment:
    """A single compartment that can hold at most one package of a given size."""

    def __init__(self, size: Size):
        """Create an empty compartment with the given size."""
        self._size = size
        self._package: Package | None = None

    def add_package(self, package: Package):
        """Store a package in this compartment. Raises ValueError if already occupied."""
        if self._package is not None:
            raise ValueError("Compartment is already occupied")
        self._package = package

    def remove_package(self):
        """Clear the compartment. Raises ValueError if not occupied."""
        if self._package is None:
            raise ValueError("Compartment is not occupied")
        self._package = None

    def get_package(self):
        """Return the package in this compartment, or None if empty."""
        return self._package

    def is_occupied(self):
        """Return True if this compartment holds a package."""
        return self._package is not None

    def get_size(self):
        """Return the size of this compartment."""
        return self._size

    def __str__(self):
        return f"Compartment(size={self._size}, package={self._package})"