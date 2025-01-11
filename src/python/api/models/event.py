from dataclasses import dataclass
from typing import final

from api.models.participant_size import ParticipantSize
from api.models.room_type import RoomType
from api.models.term import Term
from api.models.day import Day


@dataclass(frozen=True, kw_only=True)
@final
class Event:
    """Represents an `Event` of the Fachhochschule (FH) or Berufsfachschule (BFS) Wedel, such as
    a lecture, exercise, practical course, seminar or tutorial.

    Attributes:
        name: Non-empty name of the `Event`.
        employee_ids: List of zero or more ids of the employees holding the `Event`.
        participants: Dictionary of participating courses that maps course ids to a list of relevant
            semester ids.
        weekly_blocks: Positive number of weekly blocks of the `Event`.
        term: `Term` in which this `Event` takes place.
        participant_size: `ParticipantSize` of the `Event`.
        room_type: `RoomType` necessary for the `Event`.
        disallowed_days: List of days the `Event` is not allowed to be on.
    """

    name: str
    employee_ids: list[int]
    participants: dict[int, list[int]]
    weekly_blocks: int
    term: Term
    participant_size: ParticipantSize
    room_type: RoomType
    disallowed_days: list[Day]

    def __post_init__(self) -> None:
        """Validates this `EventDTO` after it has been initialized.

        Raises:
            `ValueError`: If `name` is empty or `weekly_blocks` is negative.
        """
        if not self.name:
            raise ValueError("Name must not be empty.")
        if self.weekly_blocks < 0:
            raise ValueError(
                f'Invalid number of weekly blocks "{self.weekly_blocks}". '
                + "It must be a positive integer."
            )
