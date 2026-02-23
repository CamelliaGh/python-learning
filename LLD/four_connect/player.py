class Player:
    """A Four Connect player with a name and disc color."""

    def __init__(self, name, disc_color):
        """Initialize a player.

        Args:
            name: Display name for the player.
            disc_color: Color/label used for this player's discs on the board.
        """
        self._name = name
        self._disc_color = disc_color

    def get_name(self):
        """Return this player's display name."""
        return self._name

    def get_disc_color(self):
        """Return this player's disc color (symbol used on the board)."""
        return self._disc_color