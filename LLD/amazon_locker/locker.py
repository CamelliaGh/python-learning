from compartment import Compartment
from package import Package, Size
from access_token import AccessToken


class Locker:
    """A locker containing compartments for storing packages and issuing access codes."""

    def __init__(self, compartments: list[Compartment] | None = None):
        """Initialize the locker with an optional list of compartments."""
        self._compartments = compartments if compartments is not None else []
        self._access_tokens: dict[str, AccessToken] = {}

    def add_compartment(self, compartment: Compartment):
        """Add a compartment to this locker."""
        self._compartments.append(compartment)

    def remove_compartment(self, compartment: Compartment):
        """Remove a compartment from this locker."""
        self._compartments.remove(compartment)

    def get_a_suitable_compartment(self, size: Size):
        """Return the first free compartment that fits the given size (exact match first, then larger)."""
        for compartment in self._compartments:
            if compartment.get_size() == size and not compartment.is_occupied():
                return compartment
        for compartment in self._compartments:
            if compartment.get_size() > size and not compartment.is_occupied():
                return compartment
        return None

    def allocate_package(self, package: Package) -> str:
        """Store a package in a suitable compartment and return an access code for pickup."""
        compartment = self.get_a_suitable_compartment(package.get_size())
        if compartment is None:
            raise ValueError("No compartment available")
        compartment.add_package(package)
        access_token = AccessToken(compartment)
        self._access_tokens[access_token.get_code()] = access_token
        return access_token.get_code()

    def deallocate_package(self, code: str) -> Compartment:
        """Validate the code, remove the package, and return the compartment so the device can open it."""
        if code not in self._access_tokens:
            raise ValueError("Invalid access token")
        access_token = self._access_tokens[code]
        if access_token.is_expired():
            raise ValueError("Access token expired")

        compartment = access_token.compartment
        compartment.remove_package()
        del self._access_tokens[code]
        return compartment


if __name__ == "__main__":
    locker = Locker()
    locker.add_compartment(Compartment(Size.SMALL))
    locker.add_compartment(Compartment(Size.MEDIUM))
    locker.add_compartment(Compartment(Size.LARGE))
    
    # allocate a few packages
    access_token = locker.allocate_package(Package(1, Size.SMALL))
    print(f"Allocated package 1: {access_token}")
    access_token = locker.allocate_package(Package(2, Size.MEDIUM))
    print(f"Allocated package 2: {access_token}")
    access_token = locker.allocate_package(Package(3, Size.LARGE))
    print(f"Allocated package 3: {access_token}")

    # deallocate a package
    package = locker.deallocate_package(access_token)
    print(f"Deallocated package: {package}")

    # try to deallocate a package that is not allocated
    try:
        package = locker.deallocate_package("invalid_access_token")
        print(f"Deallocated package: {package}")
    except ValueError as e:
        print(f"Error: {e}")

    # try to deallocate a package that has expired
    try:
        package = locker.deallocate_package(access_token)
        print(f"Deallocated package: {package}")
    except ValueError as e:
        print(f"Error: {e}")