from dataclasses import dataclass
from typing import final


@dataclass(frozen=True, kw_only=True)
@final
class EmployeeHoldsEventDTO:
    """Represents a Data Transfer Object (DTO) for an `Employee` holding a certain `Event`.

    Attributes:
        employee_id: Id of the related `Employee`.
        event_id: Id of the related `Event`.
    """

    employee_id: int
    event_id: int

    def __post_init__(self) -> None:
        """Validates this `EmployeeHoldsEventDTO` after it has been initialized.

        Raises:
            `ValueError`: If `employee_id` or `event_id` is less than one, which cannot possibly be
                a valid id.
        """
        if self.employee_id < 1:
            raise ValueError(f'"{self.employee_id}" is not a valid employee id.')
        if self.event_id < 1:
            raise ValueError(f'"{self.event_id}" is not a valid event id.')
