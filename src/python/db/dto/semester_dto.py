from dataclasses import dataclass
from typing import final

from api.models import semester


@dataclass(frozen=True, kw_only=True)
@final
class SemesterDTO:
    """Represents a Data Transfer Object (DTO) for a `Semester`.

    Attributes:
        id: Positive internal id in the database.
        value: Positive value which must be between 1 and 7 (inclusive).
    """

    id: int
    value: int

    def __post_init__(self) -> None:
        """Validates this `SemesterDTO` after it has been initialized.

        Raises:
            `ValueError`: If `id` is negative or `value` is outside the valid range.
        """
        if self.id < 0:
            raise ValueError(f'Invalid id "{self.id}". It must be a positive integer.')
        if (self.value < semester.MIN_VALUE) or (self.value > semester.MAX_VALUE):
            raise ValueError(
                f'Invalid value "{self.value}". '
                + f"It must be between {semester.MIN_VALUE} and {semester.MAX_VALUE} (inclusive)."
            )
