from dataclasses import dataclass
from typing import final


@dataclass(frozen=True, kw_only=True)
@final
class DateDTO:
    """Represents a Data Transfer Object (DTO) for a `Date`.

    Attributes:
        id: Postive internal id in the database.
        day_id: Id of the related `Day`.
        time_slot_id: Id of the related `TimeSlot`.
    """

    id: int
    day_id: int
    time_slot_id: int

    def __post_init__(self) -> None:
        """Validates this `DateDTO` after it has been initialized.

        Raises:
            `ValueError`: If `id` is negative or `day_id` or `time_slot_id` is less than one,
                which cannot possibly be a valid id.
        """
        if self.id < 0:
            raise ValueError(f'Invalid id "{self.id}". It must be a positive integer.')
        if self.day_id < 1:
            raise ValueError(f'"{self.day_id}" is not a valid day id.')
        if self.time_slot_id < 1:
            raise ValueError(f'"{self.time_slot_id}" is not a valid time slot id.')
