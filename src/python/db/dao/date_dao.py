import logging
from sqlite3 import Row
from typing import final, override

from db.dao.single_key_dao import SingleKeyDAO
from db.dto.date_dto import DateDTO


@final
class DateDAO(SingleKeyDAO[DateDTO]):
    """Represents a Data Access Object (DAO) for managing objects of type `DateDTO`.

    It is implemented as a singleton, meaning that only one instance of this class exists at
    runtime. Note that this class is not thread-safe in any way.
    """

    @override
    def __init__(self) -> None:
        """Initializes a `DateDAO`.

        It additionally creates the corresponding database table if it does not exist yet.

        Note that this method will only initialize the one and only instance at runtime of the
        `DateDAO` class. All calls to this method afterwards are guaranteed to have no effect.
        """
        super().__init__(
            logger=logging.getLogger(__name__),
            table_name="date",
            create_table_query="""
                CREATE TABLE IF NOT EXISTS date (
                    id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    day_id INTEGER NOT NULL REFERENCES day(id) ON UPDATE CASCADE ON DELETE CASCADE, 
                    time_slot_id INTEGER NOT NULL REFERENCES time_slot(id) ON UPDATE CASCADE ON DELETE CASCADE,
                    UNIQUE (day_id, time_slot_id)
                );
                """,
            insert_query="""
                INSERT INTO date (day_id, time_slot_id)
                VALUES (:day_id, :time_slot_id);
                """,
            select_query="""
                SELECT id, day_id, time_slot_id
                FROM date
                WHERE id = :id;
                """,
            select_all_query="""
                SELECT id, day_id, time_slot_id
                FROM date;
                """,
            update_query="""
                UPDATE date
                SET day_id = :day_id, time_slot_id = :time_slot_id
                WHERE id = :id;
                """,
            delete_query="""
                DELETE
                FROM date
                WHERE id = :id;
                """,
        )

    @override
    def _parse_row(self, row: Row) -> DateDTO:
        """Parses a `DateDTO` from a given row.

        Args:
            row: Row to parse a `DateDTO` from.

        Returns:
            A `DateDTO` parsed from the given row.
        """
        return DateDTO(id=row[0], day_id=row[1], time_slot_id=row[2])
