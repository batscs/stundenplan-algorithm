from dataclasses import dataclass
from typing import Any, final


@dataclass(frozen=True, kw_only=True)
@final
class ParticipantSize:
    """Represents a `ParticipantSize` used for estimating the capacity of a `Room` or the number of
    students participating in a certain `Event`.

    Attributes:
        name: Non-empty name of the `ParticipantSize`.
        ordinal: Positive ordinal value for the purpose of comparing different participant sizes.
    """

    name: str
    ordinal: int

    def __post_init__(self) -> None:
        """Validates this `ParticipantSize` after it has been initialized.

        Raises:
            `ValueError`: If `name` is empty or `ordinal` is negative.
        """
        if not self.name:
            raise ValueError("Name must not be empty.")
        if self.ordinal < 0:
            raise ValueError(
                f'Invalid ordinal value "{self.ordinal}". It must be a positive integer.'
            )

    def __eq__(self, other: Any) -> bool:
        """Determines if this `ParticipantSize` is equal to a given object.

        Args:
            other: Object to compare this instance with.

        Returns:
            `True` if the given objects is a `ParticipantSize` and equal to this instance,
                otherwise `False`.

        Raises:
            TypeError: If `other` is not a `ParticipantSize`.
        """
        if isinstance(other, ParticipantSize):
            return self.ordinal == other.ordinal
        raise TypeError(f"Cannot compare ParticipantSize with {type(other).__name__}.")

    def __ne__(self, other: Any) -> bool:
        """Determines if this `ParticipantSize` is not equal to a given object.

        Args:
            other: Object to compare this instance with.

        Returns:
            `True` if the given objects is a `ParticipantSize` and not equal to this instance,
                otherwise `False`.

        Raises:
            TypeError: If `other` is not a `ParticipantSize`.
        """
        if isinstance(other, ParticipantSize):
            return self.ordinal != other.ordinal
        raise TypeError(f"Cannot compare ParticipantSize with {type(other).__name__}.")

    def __lt__(self, other: Any) -> bool:
        """Determines if this `ParticipantSize` is less than a given object.

        Args:
            other: Object to compare this instance with.

        Returns:
            `True` if the given objects is a `ParticipantSize` and less than this instance,
                otherwise `False`.

        Raises:
            TypeError: If `other` is not a `ParticipantSize`.
        """
        if isinstance(other, ParticipantSize):
            return self.ordinal < other.ordinal
        raise TypeError(f"Cannot compare ParticipantSize with {type(other).__name__}.")

    def __le__(self, other: Any) -> bool:
        """Determines if this `ParticipantSize` is less than or equal to a given object.

        Args:
            other: Object to compare this instance with.

        Returns:
            `True` if the given objects is a `ParticipantSize` and less than or equal to this
                instance, otherwise `False`.

        Raises:
            TypeError: If `other` is not a `ParticipantSize`.
        """
        if isinstance(other, ParticipantSize):
            return self.ordinal <= other.ordinal
        raise TypeError(f"Cannot compare ParticipantSize with {type(other).__name__}.")

    def __gt__(self, other: Any) -> bool:
        """Determines if this `ParticipantSize` is greater than a given object.

        Args:
            other: Object to compare this instance with.

        Returns:
            `True` if the given objects is a `ParticipantSize` and greater than this instance,
                otherwise `False`.

        Raises:
            TypeError: If `other` is not a `ParticipantSize`.
        """
        if isinstance(other, ParticipantSize):
            return self.ordinal > other.ordinal
        raise TypeError(f"Cannot compare ParticipantSize with {type(other).__name__}.")

    def __ge__(self, other: Any) -> bool:
        """Determines if this `ParticipantSize` is greater than or equal to a given object.

        Args:
            other: Object to compare this instance with.

        Returns:
            `True` if the given objects is a `ParticipantSize` and greater than or equal to this
                instance, otherwise `False`.

        Raises:
            TypeError: If `other` is not a `ParticipantSize`.
        """
        if isinstance(other, ParticipantSize):
            return self.ordinal >= other.ordinal
        raise TypeError(f"Cannot compare ParticipantSize with {type(other).__name__}.")
