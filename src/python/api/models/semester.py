from dataclasses import dataclass
from typing import final

MIN_VALUE: int = 1
"""Minimum allowed value for a `Semester`."""

MAX_VALUE: int = 7
"""Maximum allowed value for a `Semester`."""


@dataclass(frozen=True, kw_only=True)
@final
class Semester:
    """Represents a numeric `Semester` related to courses and events.

    Attributes:
        value: Positive value which must be between 1 and 7 (inclusive).
    """

    value: int

    def __post_init__(self) -> None:
        """Validates this `Semester` after it has been initialized.

        Raises:
            `ValueError`: If `value` is outside the valid range.
        """
        if (self.value < MIN_VALUE) or (self.value > MAX_VALUE):
            raise ValueError(
                f'Invalid value "{self.value}". '
                + f"It must be between {MIN_VALUE} and {MAX_VALUE} (inclusive)."
            )
