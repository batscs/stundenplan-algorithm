import re
from dataclasses import dataclass
from typing import Optional, final


@dataclass(frozen=True, kw_only=True)
@final
class EmployeeDTO:
    """Represents a Data Transfer Object (DTO) for an `Employee`.

    Attributes:
        id: Positive internal id in the database.
        abbreviation: Abbreviation which consists of only uppercase letters by convention.
        title: Optional title.
        first_name: A non-empty first name. If an `Employee` has more than one first
            name, the remaining ones must be stored in `first_name` too.
        last_name: Non-empty last name.
        employee_type_id: Id of the related `EmployeeType`.
    """

    id: int
    abbreviation: str
    title: Optional[str]
    first_name: str
    last_name: str
    employee_type_id: int

    def __post_init__(self) -> None:
        """Validates this `EmployeeDTO` after it has been initialized.

        Raises:
            `ValueError`: If `id` is negative, `abbreviation` does not consist of only uppercase
                letters, `first_name` or `last_name` is empty or `employee_type_id` is less than
                one, which cannot possibly be a valid id.
        """
        if self.id < 0:
            raise ValueError(f'Invalid id "{self.id}". It must be a positive integer.')
        if re.match("[A-Z]+", self.abbreviation) is None:
            raise ValueError(
                f'Invalid abbreviation "{self.abbreviation}". '
                + "It must consist of only uppercase letters."
            )
        if not self.first_name:
            raise ValueError("First name must not be empty.")
        if not self.last_name:
            raise ValueError("Last name must not be empty.")
        if self.employee_type_id < 1:
            raise ValueError(
                f'"{self.employee_type_id}" is not a valid employee type id.'
            )
