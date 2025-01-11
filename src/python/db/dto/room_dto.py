import re
from dataclasses import dataclass
from typing import final


@dataclass(frozen=True, kw_only=True)
@final
class RoomDTO:
    """Represents a Data Transfer Object (DTO) for a `Room`.

    Attributes:
        id: Positive internal id in the database.
        abbreviation: Abbreviation which must begin with at least one uppercase letter, followed by
            any number of digits, as in "OL01", "HS07" or "SR08".
        name: Non-empty name of the `Room`.
        participant_size_id: Id of the corresponding `ParticipantSize`.
        room_type_id: Id of the corresponding `RoomType`.
    """

    id: int
    abbreviation: str
    name: str
    participant_size_id: int
    room_type_id: int

    def __post_init__(self) -> None:
        """Validates this `RoomDTO` after it has been initialized.

        Raises:
            `ValueError`: If `id` is negative, `abbreviation` has an invalid format, `name` is
                empty, or `participant_size_id` or `room_type_id` is less than one, which cannot
                possibly be a valid id.
        """
        if self.id < 0:
            raise ValueError(f'Invalid id "{self.id}". It must be a positive integer.')
        if re.match("[A-Z]+\\d*", self.abbreviation) is None:
            raise ValueError(
                f'Invalid abbreviation "{self.abbreviation}". '
                + "It must begin with at least one uppercase letter, followed by any number of digits."
            )
        if not self.name:
            raise ValueError("Name must not be empty.")
        if self.participant_size_id < 1:
            raise ValueError(
                f'"{self.participant_size_id}" is not a valid participant size id.'
            )
        if self.room_type_id < 1:
            raise ValueError(f'"{self.room_type_id}" is not a valid room type id.')
