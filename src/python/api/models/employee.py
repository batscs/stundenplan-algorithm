import re
from dataclasses import dataclass
from typing import Optional, final

from api.models.employee_type import EmployeeType


@dataclass(frozen=True, kw_only=True)
@final
class Employee:
    """Represents an `Employee` of the Fachhochschule (FH) or Berufsfachschule (BFS) Wedel.

    Attributes:
        abbreviation: Abbreviation which consists of only uppercase letters by convention.
        title: Optional title.
        first_name: A non-empty first name. If an `Employee` has more than one first
            name, the remaining ones must be stored in `first_name` too.
        last_name: Non-empty last name.
        employee_type: Corresponding `EmployeeType` of the `Employee`.
    """

    abbreviation: str
    title: Optional[str]
    first_name: str
    last_name: str
    employee_type: EmployeeType

    def __post_init__(self) -> None:
        """Validates this `Employee` after it has been initialized.

        Raises:
            `ValueError`: If `abbreviation` does not consist of only uppercase letters or
                `first_name` or `last_name` is empty.
        """
        if re.match("[A-Z]+", self.abbreviation) is None:
            raise ValueError(
                f'Invalid abbreviation "{self.abbreviation}". '
                + "It must consist of only uppercase letters."
            )
        if not self.first_name:
            raise ValueError("First name must not be empty.")
        if not self.last_name:
            raise ValueError("Last name must not be empty.")
