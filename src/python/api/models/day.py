from dataclasses import dataclass
from typing import final


ABBREVIATIONS: list[str] = ["MO", "DI", "MI", "DO", "FR", "SA", "SO"]
"""List of all allowed abbreviations for a `Day`."""

NAMES: list[str] = [
    "Montag",
    "Dienstag",
    "Mittwoch",
    "Donnerstag",
    "Freitag",
    "Samstag",
    "Sonntag",
]
"""List of all allowed names for a `Day`."""


@dataclass(frozen=True, kw_only=True)
@final
class Day:
    """Represents a `Day` of the week.

    Attributes:
        abbreviation: Abbreviation of this `Day`, which must be one of the `ABBREVIATIONS` list.
        name: Full name of this `Day`, which must be one of the `NAMES` list.
    """

    abbreviation: str
    name: str

    def __post_init__(self) -> None:
        """Validates this `Day` after it has been initialized.

        Raises:
            `ValueError`: If `abbreviation` is not one of the `ABBREVIATIONS` list or `name` is not
                one of the `NAMES` list.
        """
        if self.abbreviation not in ABBREVIATIONS:
            raise ValueError(
                f'Invalid abbreviation "{self.abbreviation}". '
                + f"It must be one of {ABBREVIATIONS}."
            )
        if self.name not in NAMES:
            raise ValueError(f'Invalid name "{self.name}". It must be one of {NAMES}.')
