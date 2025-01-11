from dataclasses import dataclass
from typing import final

from api.models.day import Day
from api.models.time_slot import TimeSlot


@dataclass(frozen=True, kw_only=True)
@final
class Date:
    """Represents a combination of a `Day` and `TimeSlot` into a single `Date`.

    Attributes:
        day: `Day` of the `Date`.
        time_slot: `TimeSlot` of the `Date`.
    """

    day: Day
    time_slot: TimeSlot
