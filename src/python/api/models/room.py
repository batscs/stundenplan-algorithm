import re
from dataclasses import dataclass
from typing import final

from api.models.participant_size import ParticipantSize
from api.models.room_type import RoomType


@dataclass(frozen=True, kw_only=True)
@final
class Room:
    """Represents a `Room` of the Fachhochschule (FH) or Berufsfachschule (BFS) Wedel in which an
    `Event` may take place.

    Attributes:
        abbreviation: Abbreviation which must begin with at least one uppercase letter, followed by
            any number of digits, as in "OL01", "HS07" or "SR08".
        name: Non-empty name of the `Room`.
        participant_size: Corresponding `ParticipantSize` of the `Room`.
        room_type: Corresponding `RoomType` of the `Room`.
    """

    abbreviation: str
    name: str
    participant_size: ParticipantSize
    room_type: RoomType

    def __post_init__(self) -> None:
        """Validates this `Room` after it has been initialized.

        Raises:
            `ValueError`: If `abbreviation` has an invalid format or `name` is empty.
        """
        if re.match("[A-Z]+\\d*", self.abbreviation) is None:
            raise ValueError(
                f'Invalid abbreviation "{self.abbreviation}". '
                + "It must begin with at least one uppercase letter, followed by any number of digits."
            )
        if not self.name:
            raise ValueError("Name must not be empty.")
