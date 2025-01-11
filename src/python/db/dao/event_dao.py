import logging
from sqlite3 import Row
from typing import final, override

from db.dao.single_key_dao import SingleKeyDAO
from db.dto.event_dto import EventDTO


@final
class EventDAO(SingleKeyDAO[EventDTO]):
    """Represents a Data Access Object (DAO) for managing objects of type `EventDTO`.

    It is implemented as a singleton, meaning that only one instance of this class exists at
    runtime. Note that this class is not thread-safe in any way.
    """

    @override
    def __init__(self) -> None:
        """Initializes an `EventDAO`.

        It additionally creates the corresponding database table if it does not exist yet.

        Note that this method will only initialize the one and only instance at runtime of the
        `EventDAO` class. All calls to this method afterwards are guaranteed to have no effect.
        """
        super().__init__(
            logger=logging.getLogger(__name__),
            table_name="event",
            create_table_query="""
                CREATE TABLE IF NOT EXISTS event (
                    id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    name TEXT NOT NULL,
                    weekly_blocks INTEGER NOT NULL,
                    term_id INTEGER NOT NULL REFERENCES term(id) ON UPDATE CASCADE ON DELETE CASCADE,
                    participant_size_id INTEGER NOT NULL REFERENCES participant_size(id) ON UPDATE CASCADE ON DELETE CASCADE,
                    room_type_id INTEGER NOT NULL REFERENCES room_type(id) ON UPDATE CASCADE ON DELETE CASCADE
                );
                """,
            insert_query="""
                INSERT INTO event (name, weekly_blocks, term_id, participant_size_id, room_type_id)
                VALUES (:name, :weekly_blocks, :term_id, :participant_size_id, :room_type_id);
                """,
            select_query="""
                SELECT id, name, weekly_blocks, term_id, participant_size_id, room_type_id
                FROM event
                WHERE id = :id;
                """,
            select_all_query="""
                SELECT id, name, weekly_blocks, term_id, participant_size_id, room_type_id
                FROM event;
                """,
            update_query="""
                UPDATE event
                SET name = :name, weekly_blocks = :weekly_blocks, term_id = :term_id, participant_size_id = :participant_size_id, room_type_id = :room_type_id
                WHERE id = :id;
                """,
            delete_query="""
                DELETE
                FROM event
                WHERE id = :id;
                """,
        )

    @override
    def _parse_row(self, row: Row) -> EventDTO:
        """Parses an `EventDTO` from a given row.

        Args:
            row: Row to parse an `EventDTO` from.

        Returns:
            An `EventDTO` parsed from the given row.
        """
        return EventDTO(
            id=row[0],
            name=row[1],
            weekly_blocks=row[2],
            term_id=row[3],
            participant_size_id=row[4],
            room_type_id=row[5],
        )
