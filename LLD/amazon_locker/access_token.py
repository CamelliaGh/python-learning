from datetime import datetime, timedelta
from uuid import uuid4
from compartment import Compartment


class AccessToken:
    """A time-limited code that authorizes pickup from a specific compartment."""

    def __init__(self, compartment: Compartment):
        """Create an access token for the given compartment (valid for 7 days)."""
        self._code = str(uuid4())
        self._start_time = datetime.now()
        self._compartment = compartment
        self._end_time = self._start_time + timedelta(days=7)

    def is_expired(self):
        """Return True if this token is past its validity period."""
        return datetime.now() > self._end_time

    def get_code(self):
        """Return the pickup code for the customer."""
        return self._code

    @property
    def compartment(self) -> Compartment:
        """The compartment this token authorizes access to."""
        return self._compartment

    def __str__(self):
        return f"AccessToken(code={self._code}, start_time={self._start_time}, end_time={self._end_time}, compartment={self._compartment})"