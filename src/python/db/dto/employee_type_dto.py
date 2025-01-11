from dataclasses import dataclass
from typing import final


@dataclass(frozen=True, kw_only=True)
@final
class EmployeeTypeDTO:
    """Represents a Data Transfer Object (DTO) for an `EmployeeType`.

    Attributes:
        id: Positive internal id in the database.
        name: Non-empty name of the `EmployeeType`.
    """

    id: int
    name: str

    def __post_init__(self) -> None:
        """Validates this `EmployeeTypeDTO` after it has been initialized.

        Raises:
            `ValueError`: If `id` is negative or `name` is empty.
        """
        if self.id < 0:
            raise ValueError(f'Invalid id "{self.id}". It must be a positive integer.')
        if not self.name:
            raise ValueError("Name must not be empty.")
