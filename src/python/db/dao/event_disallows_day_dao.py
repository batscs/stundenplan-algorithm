import logging
from sqlite3 import Row
from typing import final, override

from db.dao.double_key_dao import DoubleKeyDAO
from db.dto.event_disallows_day_dto import EventDisallowsDayDTO


@final
class EventDisallowsDayDAO(DoubleKeyDAO[EventDisallowsDayDTO]):
    """Represents a Data Access Object (DAO) for managing objects of type `EventDisallowsDayDTO`.

    It is implemented as a singleton, meaning that only one instance of this class exists at
    runtime. Note that this class is not thread-safe in any way.
    """

    @override
    def __init__(self) -> None:
        """Initializes an `EventDisallowsDayDAO`.

        It additionally creates the corresponding database table if it does not exist yet.

        Note that this method will only initialize the one and only instance at runtime of the
        `EventDisallowsDayDAO` class. All calls to this method afterwards are guaranteed to have no
        effect.
        """
        super().__init__(
            logger=logging.getLogger(__name__),
            table_name="event_disallows_day",
            create_table_query="""
               CREATE TABLE IF NOT EXISTS event_disallows_day (
                   event_id INTEGER NOT NULL REFERENCES event(id) ON UPDATE CASCADE ON DELETE CASCADE, 
                   day_id INTEGER NOT NULL REFERENCES day(id) ON UPDATE CASCADE ON DELETE CASCADE,
                   PRIMARY KEY (event_id, day_id)
               );
               """,
            insert_query="""
               INSERT INTO event_disallows_day (event_id, day_id)
               VALUES (:event_id, :day_id);
               """,
            select_query="""
               SELECT event_id, day_id
               FROM event_disallows_day
               WHERE event_id = :first_id AND day_id = :second_id;
               """,
            select_all_query="""
               SELECT event_id, day_id
               FROM event_disallows_day;
               """,
            update_query="""
               UPDATE event_disallows_day
               SET event_id = :event_id, day_id = :day_id 
               WHERE event_id = :event_id AND day_id = :day_id;
               """,
            delete_query="""
               DELETE FROM event_disallows_day
               WHERE event_id = :first_id AND day_id = :second_id;
               """,
        )

    @override
    def _parse_row(self, row: Row) -> EventDisallowsDayDTO:
        """Parses an `EventDisallowsDayDTO` from a given row.

        Args:
            row: Row to parse an `EventDisallowsDayDTO` from.

        Returns:
            An `EventDisallowsDayDTO` parsed from the given row.
        """
        return EventDisallowsDayDTO(event_id=row[0], day_id=row[1])
