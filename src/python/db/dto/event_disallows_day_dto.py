from dataclasses import dataclass
from typing import final


@dataclass(frozen=True, kw_only=True)
@final
class EventDisallowsDayDTO:
    """Represents a Data Transfer Object (DTO) for an `Event` which is not allowed on a certain day.

    Attributes:
        event_id: Id of the related `Event`.
        day_id: Id of the related `Day`.
    """

    event_id: int
    day_id: int

    def __post_init__(self) -> None:
        """Validates this `EventDisallowsDayDTO` after it has been initialized.

        Raises:
            `ValueError`: If `event_id` or `day_id` is less than one, which cannot possibly be
                a valid id.
        """
        if self.event_id < 1:
            raise ValueError(f'"{self.event_id}" is not a valid event id.')
        if self.day_id < 1:
            raise ValueError(f'"{self.day_id}" is not a valid day id.')
