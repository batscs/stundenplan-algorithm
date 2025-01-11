from dataclasses import dataclass
from typing import final


@dataclass(frozen=True, kw_only=True)
@final
class EmployeeType:
    """Represents an `EmployeeType` of an `Employee`.

    Attributes:
        name: Non-empty name of the `EmployeeType`.
    """

    name: str

    def __post_init__(self) -> None:
        """Validates this `EmployeeType` after it has been initialized.

        Raises:
            `ValueError`: If `name` is empty.
        """
        if not self.name:
            raise ValueError("Name must not be empty.")
