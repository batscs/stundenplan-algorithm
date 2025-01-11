import logging
from sqlite3 import Row
from typing import final, override

from db.dao.single_key_dao import SingleKeyDAO
from db.dto.participant_size import ParticipantSizeDTO


@final
class ParticipantSizeDAO(SingleKeyDAO[ParticipantSizeDTO]):
    """Represents a Data Access Object (DAO) for managing objects of type `ParticipantSizeDTO`.

    It is implemented as a singleton, meaning that only one instance of this class exists at
    runtime. Note that this class is not thread-safe in any way.
    """

    @override
    def __init__(self) -> None:
        """Initializes a `ParticipantSizeDAO`.

        It additionally creates the corresponding database table if it does not exist yet.

        Note that this method will only initialize the one and only instance at runtime of the
        `ParticipantSizeDAO` class. All calls to this method afterwards are guaranteed to have no
        effect.
        """
        super().__init__(
            logger=logging.getLogger(__name__),
            table_name="participant_size",
            create_table_query="""
                CREATE TABLE IF NOT EXISTS participant_size (
                    id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    name TEXT NOT NULL UNIQUE,
                    ordinal INTEGER NOT NULL UNIQUE
                );
                """,
            insert_query="""
                INSERT INTO participant_size (name, ordinal)
                VALUES (:name, :ordinal);
                """,
            select_query="""
                SELECT id, name, ordinal
                FROM participant_size
                WHERE id = :id;
                """,
            select_all_query="""
                SELECT id, name, ordinal
                FROM participant_size;
                """,
            update_query="""
                UPDATE participant_size
                SET name = :name, ordinal = :ordinal
                WHERE id = :id;
                """,
            delete_query="""
                DELETE
                FROM participant_size
                WHERE id = :id;
                """,
        )

    @override
    def _parse_row(self, row: Row) -> ParticipantSizeDTO:
        """Parses a `ParticipantSizeDTO` from a given row.

        Args:
            row: Row to parse a `ParticipantSizeDTO` from.

        Returns:
            A `ParticipantSizeDTO` parsed from the given row.
        """
        return ParticipantSizeDTO(id=row[0], name=row[1], ordinal=row[2])
