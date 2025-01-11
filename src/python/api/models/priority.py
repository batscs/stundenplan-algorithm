from dataclasses import dataclass
from typing import final

MIN_VALUE: int = 1
"""Minimum allowed value for a `Priority`."""

MAX_VALUE: int = 100
"""Maximum allowed value for a `Priority`."""


@dataclass(frozen=True, kw_only=True)
@final
class Priority:
    """Represents a `Priority` used for generating the time schedule.

    Attributes:
        value: Positive value which must be between 1 and 100 (inclusive).
    """

    value: int

    def __post_init__(self) -> None:
        """Validates this `Priority` after it has been initialized.

        Raises:
            `ValueError`: If `value` is outside the valid range.
        """
        if (self.value < MIN_VALUE) or (self.value > MAX_VALUE):
            raise ValueError(
                f'Invalid value "{self.value}". '
                + f"It must be between {MIN_VALUE} and {MAX_VALUE} (inclusive)."
            )
