from datetime import time

HOURS_PER_DAY: int = 24
"""Number of hours in a single day."""

MINUTES_PER_HOUR: int = 60
"""Number of minutes in a single hour."""

SECONDS_PER_HOUR: int = 3600
"""Number of seconds in a single hour."""

SECONDS_PER_MINUTE: int = 60
"""Number of seconds in a single minute."""

MAX_MINUTES_PER_DAY: int = ((HOURS_PER_DAY - 1) * MINUTES_PER_HOUR) + (
    MINUTES_PER_HOUR - 1
)
"""Maximum number of minutes in a single day ((23 * 60) + 59 = 1439)."""


def time_to_minutes(time: time) -> int:
    """Converts a given `time` object to minutes since midnight.

    Note that this function only considers the `time` objects `hour` and `minute` attributes,
    all others are ignored.

    Args:
        time: The `time` object to convert.

    Returns:
        The number of minutes since midnight equivalent to the given `time` object.
    """
    return (time.hour * MINUTES_PER_HOUR) + time.minute


def minutes_to_time(minutes_since_midnight: int) -> time:
    """Converts a given number of minutes since midnight to a `time` object.

    Args:
        minutes_since_midnight: Number of minutes since midnight to convert.

    Returns:
        A `time` object equivalent to the given number of minutes since midnight.

    Raises:
        `ValueError`: When `minutes_since_midnight` is negative or greater than
            `MAX_MINUTES_PER_DAY`.
    """
    if (minutes_since_midnight < 0) or (minutes_since_midnight > MAX_MINUTES_PER_DAY):
        raise ValueError(
            f'Invalid number of minutes since midnight "{minutes_since_midnight}". '
            + f"It must be between 0 and {MAX_MINUTES_PER_DAY} (inclusive)."
        )
    hour, minute = divmod(minutes_since_midnight, MINUTES_PER_HOUR)
    return time(hour, minute)


def seconds_to_formatted_duration(seconds: float) -> str:
    """Converts a given number of seconds into a formatted string with hours, minutes and seconds.

    Args:
        seconds: Number of seconds to convert.

    Returns:
        A string with the format "HH:MM:SS".
    """
    hours, remainder = divmod(seconds, SECONDS_PER_HOUR)
    minutes, seconds = divmod(remainder, SECONDS_PER_MINUTE)
    return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"
