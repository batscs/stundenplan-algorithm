from dataclasses import dataclass
from typing import final


@dataclass(frozen=True, kw_only=True)
@final
class CourseContainsEventDTO:
    """Represents a Data Transfer Object (DTO) for a `Course` which contains a certain `Event`
    within a certain `Semester`.

    Attributes:
        course_id: Id of the related `Course`.
        semester_id: Id of the related `Semester`.
        event_id: Id of the related `Event`.
    """

    course_id: int
    semester_id: int
    event_id: int

    def __post_init__(self) -> None:
        """Validates this `CourseContainsEventDTO` after it has been initialized.

        Raises:
            `ValueError`: If `course_id`, `semester_id` or `event_id` is less than one, since that
                cannot possibly be a valid id.
        """
        if self.course_id < 1:
            raise ValueError(f'"{self.course_id}" is not a valid course id.')
        if self.semester_id < 1:
            raise ValueError(f"{self.semester_id} is not a valid semester id.")
        if self.event_id < 1:
            raise ValueError(f'"{self.event_id}" is not a valid event id.')
