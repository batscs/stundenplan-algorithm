import logging
from sqlite3 import Row
from typing import final, override

from db.dao.single_key_dao import SingleKeyDAO
from db.dto.priority_dto import PriorityDTO


@final
class PriorityDAO(SingleKeyDAO[PriorityDTO]):
    """Represents a Data Access Object (DAO) for managing objects of type `PriorityDTO`.

    It is implemented as a singleton, meaning that only one instance of this class exists at
    runtime. Note that this class is not thread-safe in any way.
    """

    @override
    def __init__(self) -> None:
        """Initializes a `PriorityDAO`.

        It additionally creates the corresponding database table if it does not exist yet.

        Note that this method will only initialize the one and only instance at runtime of the
        `PriorityDAO` class. All calls to this method afterwards are guaranteed to have no effect.
        """
        super().__init__(
            logger=logging.getLogger(__name__),
            table_name="priority",
            create_table_query="""
                CREATE TABLE IF NOT EXISTS priority (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    value INTEGER NOT NULL UNIQUE
                );
                """,
            insert_query="""
                INSERT INTO priority (value)
                VALUES (:value);
                """,
            select_query="""
                SELECT id, value
                FROM priority
                WHERE id = :id;
                """,
            select_all_query="""
                SELECT id, value
                FROM priority;
                """,
            update_query="""
                UPDATE priority
                SET value = :value
                WHERE id = :id;
                """,
            delete_query="""
                DELETE
                FROM priority
                WHERE id = :id;
                """,
        )

    @override
    def _parse_row(self, row: Row) -> PriorityDTO:
        """Parses a `PriorityDTO` from a given row.

        Args:
            row: Row to parse a `PriorityDTO` from.

        Returns:
            A `PriorityDTO` parsed from the given row.
        """
        return PriorityDTO(id=row[0], value=row[1])
