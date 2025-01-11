from dataclasses import dataclass
from typing import final

from api.models import day


@dataclass(frozen=True, kw_only=True)
@final
class DayDTO:
    """Represents a Data Transfer Object (DTO) for a `Day` of the week.

    Attributes:
        id: Positive internal id in the database.
        abbreviation: Abbreviation of this `Day`, which must be one of the `ABBREVIATIONS` list.
        name: Full name of this `Day`, which must be one of the `NAMES` list.
    """

    id: int
    abbreviation: str
    name: str

    def __post_init__(self) -> None:
        """Validates this `DayDTO` after it has been initialized.

        Raises:
            `ValueError`: If `id` is negative, `abbreviation` is not one of the `ABBREVIATIONS`
                list or `name` is not one of the `NAMES` list.
        """
        if self.id < 0:
            raise ValueError(f'Invalid id "{self.id}". It must be a positive integer.')
        if self.abbreviation not in day.ABBREVIATIONS:
            raise ValueError(
                f'Invalid abbreviation "{self.abbreviation}". '
                + f"It must be one of {day.ABBREVIATIONS}."
            )
        if self.name not in day.NAMES:
            raise ValueError(
                f'Invalid name "{self.name}". It must be one of {day.NAMES}.'
            )
