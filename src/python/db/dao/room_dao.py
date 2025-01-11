import logging
from sqlite3 import Row
from typing import final, override

from db.dao.single_key_dao import SingleKeyDAO
from db.dto.room_dto import RoomDTO


@final
class RoomDAO(SingleKeyDAO[RoomDTO]):
    """Represents a Data Access Object (DAO) for managing objects of type `RoomDTO`.

    It is implemented as a singleton, meaning that only one instance of this class exists at
    runtime. Note that this class is not thread-safe in any way.
    """

    @override
    def __init__(self) -> None:
        """Initializes a `RoomDAO`.

        It additionally creates the corresponding database table if it does not exist yet.

        Note that this method will only initialize the one and only instance at runtime of the
        `RoomDAO` class. All calls to this method afterwards are guaranteed to have no effect.
        """
        super().__init__(
            logger=logging.getLogger(__name__),
            table_name="room",
            create_table_query="""
                CREATE TABLE IF NOT EXISTS room (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    abbreviation TEXT NOT NULL UNIQUE,
                    name TEXT NOT NULL UNIQUE, 
                    participant_size_id INTEGER NOT NULL REFERENCES participant_size(id) ON UPDATE CASCADE ON DELETE CASCADE,
                    room_type_id INTEGER NOT NULL REFERENCES room_type(id) ON UPDATE CASCADE ON DELETE CASCADE
                );
                """,
            insert_query="""
                INSERT INTO room (abbreviation, name, participant_size_id, room_type_id)
                VALUES (:abbreviation, :name, :participant_size_id, :room_type_id);
                """,
            select_query="""
                SELECT id, abbreviation, name, participant_size_id, room_type_id
                FROM room
                WHERE id = :id;
                """,
            select_all_query="""
                SELECT id, abbreviation, name, participant_size_id, room_type_id
                FROM room;
                """,
            update_query="""
                UPDATE room
                SET abbreviation = :abbreviation, name = :name, participant_size_id = :participant_size_id, room_type_id = :room_type:id
                WHERE id = :id;
                """,
            delete_query="""
                DELETE
                FROM room
                WHERE id = :id;
                """,
        )

    @override
    def _parse_row(self, row: Row) -> RoomDTO:
        """Parses a `RoomDTO` from a given row.

        Args:
            row: Row to parse a `RoomDTO` from.

        Returns:
            A `RoomDTO` parsed from the given row.
        """
        return RoomDTO(
            id=row[0],
            abbreviation=row[1],
            name=row[2],
            participant_size_id=row[3],
            room_type_id=row[4],
        )
