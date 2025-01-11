from dataclasses import dataclass
from typing import final


@dataclass(frozen=True, kw_only=True)
@final
class EmployeeDislikesDateDTO:
    """Represents a Data Transfer Object (DTO) for an `Employee` disliking a certain `Date`.

    Attributes:
        employee_id: Id of the related `Employee`.
        date_id: Id of the related `Date`.
        priority_id: Id of the `Priority` associated to this relation.
    """

    employee_id: int
    date_id: int
    priority_id: int

    def __post_init__(self) -> None:
        """Validates this `EmployeeDislikesDateDTO` after it has been initialized.

        Raises:
            `ValueError`: If `employee_id`, `date_id` or `priority_id` is less than one, which
                cannot possibly be a valid id.
        """
        if self.employee_id < 1:
            raise ValueError(f'"{self.employee_id}" is not a valid employee id.')
        if self.date_id < 1:
            raise ValueError(f'"{self.date_id}" is not a valid date id.')
        if self.priority_id < 1:
            raise ValueError(f'"{self.priority_id}" is not a valid priority id.')
