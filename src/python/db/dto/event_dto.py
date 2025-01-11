from dataclasses import dataclass
from typing import final


@dataclass(frozen=True, kw_only=True)
@final
class EventDTO:
    """Represents a Data Transfer Object (DTO) for an `Event`.

    Attributes:
        id: Positive internal id in the database.
        name: Non-empty name of the `Event`.
        weekly_blocks: Positive number of weekly blocks of the `Event`.
        term_id: Id of the related `Term`.
        participant_size_id: Id of the related `ParticipantSize`.
        room_type_id: Id of the related `RoomType` necessary for the `Event`.
    """

    id: int
    name: str
    weekly_blocks: int
    term_id: int
    participant_size_id: int
    room_type_id: int

    def __post_init__(self) -> None:
        """Validates this `EventDTO` after it has been initialized.

        Raises:
            `ValueError`: If `id` is negative, `name` is empty, `weekly_blocks` is negative
                or `term_id`, `participant_size_id` or `room_type_id` is less than one, which cannot
                possibly be a valid id.
        """
        if self.id < 0:
            raise ValueError(f'Invalid id "{self.id}". It must be a positive integer.')
        if not self.name:
            raise ValueError("Name must not be empty.")
        if self.weekly_blocks < 0:
            raise ValueError(
                f'Invalid number of weekly blocks "{self.weekly_blocks}". '
                + "It must be a positive integer."
            )
        if self.term_id < 1:
            raise ValueError(f'"{self.term_id}" is not a valid term id.')
        if self.participant_size_id < 1:
            raise ValueError(
                f'"{self.participant_size_id}" is not a valid participant size id.'
            )
        if self.room_type_id < 1:
            raise ValueError(f'"{self.room_type_id}" is not a valid room type id.')
