from dataclasses import dataclass
from typing import final


@dataclass(frozen=True, kw_only=True)
@final
class RoomType:
    """Represents a `RoomType` associated to zero or more rooms of the Fachhochschule (FH)
    or Berufsfachschule (BFS) Wedel.

    Attributes:
        name: Non-empty name of the `RoomType`.
    """

    name: str

    def __post_init__(self) -> None:
        """Validates this `RoomType` after it has been initialized.

        Raises:
            `ValueError`: If `name` is empty.
        """
        if not self.name:
            raise ValueError("Name must not be empty.")
