from dataclasses import dataclass
from typing import final

NAMES: list[str] = ["Sommer", "Winter"]
"List of allowed names for a `Term`."


@dataclass(frozen=True, kw_only=True)
@final
class Term:
    """Represents a `Term` in which events may take place.

    Attributes:
        name: Non-empty name which must be either "Sommer" or "Winter".
    """

    name: str

    def __post_init__(self) -> None:
        """Validates this `Term` after it has been initialized.

        Raises:
            `ValueError`: If `name` is neither "Sommer" nor "Winter".
        """
        if self.name not in NAMES:
            raise ValueError(f'Invalid name "{self.name}". It must be one of {NAMES}.')
