import logging
from sqlite3 import Row
from typing import final, override

from db.dao.single_key_dao import SingleKeyDAO
from db.dto.semester_dto import SemesterDTO


@final
class SemesterDAO(SingleKeyDAO[SemesterDTO]):
    """Represents a Data Access Object (DAO) for managing objects of type `SemesterDTO`.

    It is implemented as a singleton, meaning that only one instance of this class exists at
    runtime. Note that this class is not thread-safe in any way.
    """

    @override
    def __init__(self) -> None:
        """Initializes a `SemesterDAO`.

        It additionally creates the corresponding database table if it does not exist yet.

        Note that this method will only initialize the one and only instance at runtime of the
        `SemesterDAO` class. All calls to this method afterwards are guaranteed to have no effect.
        """
        super().__init__(
            logger=logging.getLogger(__name__),
            table_name="semester",
            create_table_query="""
                CREATE TABLE IF NOT EXISTS semester (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    value INTEGER NOT NULL
                );
                """,
            insert_query="""
                INSERT INTO semester (value)
                VALUES (:value);
                """,
            select_query="""
                SELECT id, value
                FROM semester
                WHERE id = :id;
                """,
            select_all_query="""
                SELECT id, value
                FROM semester;
                """,
            update_query="""
                UPDATE semester
                SET value = :value
                WHERE id = :id;
                """,
            delete_query="""
                DELETE
                FROM semester
                WHERE id = :id;
                """,
        )

    @override
    def _parse_row(self, row: Row) -> SemesterDTO:
        """Parses a `SemesterDTO` from a given row.

        Args:
            row: Row to parse a `SemesterDTO` from.

        Returns:
            A `SemesterDTO` parsed from the given row.
        """
        return SemesterDTO(id=row[0], value=row[1])
