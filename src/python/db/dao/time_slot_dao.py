import logging
from sqlite3 import Row
from typing import final, override

from db.dao.single_key_dao import SingleKeyDAO
from db.dto.time_slot_dto import TimeSlotDTO


@final
class TimeSlotDAO(SingleKeyDAO[TimeSlotDTO]):
    """Represents a Data Access Object (DAO) for managing objects of type `TimeSlotDTO`.

    It is implemented as a singleton, meaning that only one instance of this class exists at
    runtime. Note that this class is not thread-safe in any way.
    """

    @override
    def __init__(self) -> None:
        """Initializes a `TimeSlotDAO`.

        It additionally creates the corresponding database table if it does not exist yet.

        Note that this method will only initialize the one and only instance at runtime of the
        `TimeSlotDAO` class. All calls to this method afterwards are guaranteed to have no effect.
        """
        super().__init__(
            logger=logging.getLogger(__name__),
            table_name="time_slot",
            create_table_query="""
                CREATE TABLE IF NOT EXISTS time_slot (
                    id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    start_time TIME NOT NULL UNIQUE,
                    end_time TIME NOT NULL UNIQUE
                );
                """,
            insert_query="""
                INSERT INTO time_slot (start_time, end_time)
                VALUES (:start_time, :end_time);
                """,
            select_query="""
                SELECT id, start_time, end_time
                FROM time_slot
                WHERE id = :id;
                """,
            select_all_query="""
                SELECT id, start_time, end_time
                FROM time_slot;
                """,
            update_query="""
                UPDATE time_slot
                SET start_time = :start_time, end_time = :end_time
                WHERE id = :id;
                """,
            delete_query="""
                DELETE
                FROM time_slot
                WHERE id = :id;
                """,
        )

    @override
    def _parse_row(self, row: Row) -> TimeSlotDTO:
        """Parses a `TimeSlotDTO` from a given row.

        Args:
            row: Row to parse a `TimeSlotDTO` from.

        Returns:
            A `TimeSlotDTO` parsed from the given row.
        """
        return TimeSlotDTO(id=row[0], start_time=row[1], end_time=row[2])
