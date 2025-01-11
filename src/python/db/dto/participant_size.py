from dataclasses import dataclass
from typing import final


@dataclass(frozen=True, kw_only=True)
@final
class ParticipantSizeDTO:
    """Represents a Data Transfer Object (DTO) for a `ParticipantSize`.

    Attributes:
        id: Positive internal id in the database.
        name: Non-empty name of the `ParticipantSize`.
        ordinal: Positive ordinal value for the purpose of comparing different participant sizes.
    """

    id: int
    name: str
    ordinal: int

    def __post_init__(self) -> None:
        """Validates this `ParticipantSizeDTO` after it has been initialized.

        Raises:
            `ValueError`: If `id` is negative, `name` is empty or `ordinal` is negative.
        """
        if self.id < 0:
            raise ValueError(f'Invalid id "{self.id}". It must be a positive integer.')
        if not self.name:
            raise ValueError("Name must not be empty.")
        if self.ordinal < 0:
            raise ValueError(
                f'Invalid ordinal value "{self.ordinal}". It must be a positive integer.'
            )
