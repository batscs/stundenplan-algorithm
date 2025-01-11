from dataclasses import dataclass
from typing import final

from api.models import priority


@dataclass(frozen=True, kw_only=True)
@final
class PriorityDTO:
    """Represents a Data Transfer Object (DTO) for a `Priority`.

    Attributes:
        id: Positive internal id in the database.
        value: Positive value which must be between 1 and 100 (inclusive).
    """

    id: int
    value: int

    def __post_init__(self) -> None:
        """Validates this `PriorityDTO` after it has been initialized.

        Raises:
            `ValueError`: If `id` is negative or `value` is outside the valid range.
        """
        if self.id < 0:
            raise ValueError(f'Invalid id "{self.id}". It must be a positive integer.')
        if (self.value < priority.MIN_VALUE) or (self.value > priority.MAX_VALUE):
            raise ValueError(
                f'Invalid value "{self.value}". '
                + f"It must be between {priority.MIN_VALUE} and {priority.MAX_VALUE} (inclusive)."
            )
