from dataclasses import dataclass
from typing import final

from api.models import term


@dataclass(frozen=True, kw_only=True)
@final
class TermDTO:
    """Represents a Data Transfer Object (DTO) for a `Term`.

    Attributes:
        id: Positive internal id in the database.
        name: Non-empty name which must be either "Sommer" or "Winter".
    """

    id: int
    name: str

    def __post_init__(self) -> None:
        """Validates this `TermDTO` after it has been initialized.

        Raises:
            `ValueError`: If `id` is negative or `name` is neither "Sommer" nor "Winter".
        """
        if self.id < 0:
            raise ValueError(f'Invalid id "{self.id}". It must be a positive integer.')
        if self.name not in term.NAMES:
            raise ValueError(
                f'Invalid name "{self.name}". It must be one of {term.NAMES}.'
            )
