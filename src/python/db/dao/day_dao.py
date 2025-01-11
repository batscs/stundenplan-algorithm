import logging
from sqlite3 import Row
from typing import final, override

from db.dao.single_key_dao import SingleKeyDAO
from db.dto.day_dto import DayDTO


@final
class DayDAO(SingleKeyDAO[DayDTO]):
    """Represents a Data Access Object (DAO) for managing objects of type `DayDTO`.

    It is implemented as a singleton, meaning that only one instance of this class exists at
    runtime. Note that this class is not thread-safe in any way.
    """

    @override
    def __init__(self) -> None:
        """Initializes a `DayDAO`.

        It additionally creates the corresponding database table if it does not exist yet.

        Note that this method will only initialize the one and only instance at runtime of the
        `DayDAO` class. All calls to this method afterwards are guaranteed to have no effect.
        """
        super().__init__(
            logger=logging.getLogger(__name__),
            table_name="day",
            create_table_query="""
                CREATE TABLE IF NOT EXISTS day (
                    id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    abbreviation TEXT NOT NULL UNIQUE,
                    name TEXT NOT NULL UNIQUE
                );
            """,
            insert_query="""
                INSERT INTO day (abbreviation, name)
                VALUES (:abbreviation, :name);
            """,
            select_query="""
                SELECT id, abbreviation, name
                FROM day
                WHERE id = :id;
            """,
            select_all_query="""
                SELECT id, abbreviation, name
                FROM day;
            """,
            update_query="""
                UPDATE day
                SET abbreviation = :abbreviation, name = :name
                WHERE id = :id;
            """,
            delete_query="""
                DELETE
                FROM day
                WHERE id = :id;
            """,
        )

    @override
    def _parse_row(self, row: Row) -> DayDTO:
        """Parses a `DayDTO` from a given row.

        Args:
            row: Row to parse a `DayDTO` from.

        Returns:
            A `DayDTO` parsed from the given row.
        """
        return DayDTO(id=row[0], abbreviation=row[1], name=row[2])
