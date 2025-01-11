from dataclasses import dataclass
from datetime import time
from typing import final


@dataclass(frozen=True, kw_only=True)
@final
class TimeSlotDTO:
    """Represents a Data Transfer Object (DTO) for a `TimeSlot`.

    Attributes:
        id: Positive internal id in the database.
        start_time: Start time which must be strictly before `end_time`. Note that only the hour and
            minute of the `time` object are used, all others are ignored.
        end_time: End time which must be strictly after `start_time`. Note that only the hour and
            minute of the `time` object are used, all others are ignored.
    """

    id: int
    start_time: time
    end_time: time

    def __post_init__(self) -> None:
        """Validates this `TimeSlotDTO` after it has been initialized.

        Raises:
            `ValueError`: If `id` is negative or `start_time` is not strictly before `end_time`.
        """
        if self.id < 0:
            raise ValueError(f'Invalid id "{self.id}". It must be a positive integer.')
        if self.start_time >= self.end_time:
            raise ValueError(
                f'Invalid start "{self.start_time}" or end "{self.end_time}" time. '
                + "Start time must be strictly before end time."
            )
