import logging
from sqlite3 import Row
from typing import final, override

from db.dao.single_key_dao import SingleKeyDAO
from db.dto.term_dto import TermDTO


@final
class TermDAO(SingleKeyDAO[TermDTO]):
    """Represents a Data Access Object (DAO) for managing objects of type `TermDTO`.

    It is implemented as a singleton, meaning that only one instance of this class exists at
    runtime. Note that this class is not thread-safe in any way.
    """

    @override
    def __init__(self) -> None:
        """Initializes a `TermDAO`.

        It additionally creates the corresponding database table if it does not exist yet.

        Note that this method will only initialize the one and only instance at runtime of the
        `TermDAO` class. All calls to this method afterwards are guaranteed to have no effect.
        """
        super().__init__(
            logger=logging.getLogger(__name__),
            table_name="term",
            create_table_query="""
                CREATE TABLE IF NOT EXISTS term (
                    id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    name TEXT NOT NULL UNIQUE
                );
                """,
            insert_query="""
                INSERT INTO term (name)
                VALUES (:name);
                """,
            select_query="""
                SELECT id, name
                FROM term
                WHERE id = :id;
                """,
            select_all_query="""
                SELECT id, name
                FROM term;
                """,
            update_query="""
                UPDATE term
                SET name = :name
                WHERE id = :id;
                """,
            delete_query="""
                DELETE
                FROM term
                WHERE id = :id;
                """,
        )

    @override
    def _parse_row(self, row: Row) -> TermDTO:
        """Parses a `TermDTO` from a given row.

        Args:
            row: Row to parse a `TermDTO` from.

        Returns:
            A `TermDTO` parsed from the given row.
        """
        return TermDTO(id=row[0], name=row[1])
