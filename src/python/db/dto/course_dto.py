import re
from dataclasses import dataclass
from typing import final


@dataclass(frozen=True, kw_only=True)
@final
class CourseDTO:
    """Represents a Data Transfer Object (DTO) for a `Course`.

    Attributes:
        id: Positive internal id in the database.
        abbreviation: Abbreviation of the `Course`, which only consists of uppercase letters or
            underscores by convention. Bachelor courses contain the prefix "B_" as in "B_INF",
            while master courses use the prefix "M_". Courses of the Berufsfachschule (BFS) Wedel do
            not use any prefix.
        name: Non-empty full name of the `Course`.
    """

    id: int
    abbreviation: str
    name: str

    def __post_init__(self) -> None:
        """Validates this `CourseDTO` after it has been initialized.

        Raises:
            `ValueError`: If `id` is negative, `abbreviation` does not consist of only uppercase
                letters or underscores, or `name` is empty.
        """
        if self.id < 0:
            raise ValueError(f'Invalid id "{self.id}". It must be a positive integer.')
        if re.match("[A-Z_]+", self.abbreviation) is None:
            raise ValueError(
                f'Invalid abbreviation "{self.abbreviation}". '
                + "It must consist of only uppercase letters or underscores."
            )
        if not self.name:
            raise ValueError("Name must not be empty.")
