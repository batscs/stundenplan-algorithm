import logging
from sqlite3 import Row
from typing import final, override

from db.dao.single_key_dao import SingleKeyDAO
from db.dto.room_type_dto import RoomTypeDTO


@final
class RoomTypeDAO(SingleKeyDAO[RoomTypeDTO]):
    """Represents a Data Access Object (DAO) for managing objects of type `RoomTypeDTO`.

    It is implemented as a singleton, meaning that only one instance of this class exists at
    runtime. Note that this class is not thread-safe in any way.
    """

    @override
    def __init__(self) -> None:
        """Initializes a `RoomTypeDAO`.

        It additionally creates the corresponding database table if it does not exist yet.

        Note that this method will only initialize the one and only instance at runtime of the
        `RoomTypeDAO` class. All calls to this method afterwards are guaranteed to have no effect.
        """
        super().__init__(
            logger=logging.getLogger(__name__),
            table_name="room_type",
            create_table_query="""
                CREATE TABLE IF NOT EXISTS room_type (
                    id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    name TEXT NOT NULL UNIQUE
                );
                """,
            insert_query="""
                INSERT INTO room_type (name)
                VALUES (:name);
                """,
            select_query="""
                SELECT id, name
                FROM room_type
                WHERE id = :id;
                """,
            select_all_query="""
                SELECT id, name
                FROM room_type;
                """,
            update_query="""
                UPDATE room_type
                SET name = :name
                WHERE id = :id;
                """,
            delete_query="""
                DELETE
                FROM room_type
                WHERE id = :id;
                """,
        )

    @override
    def _parse_row(self, row: Row) -> RoomTypeDTO:
        """Parses a `RoomTypeDTO` from a given row.

        Args:
            row: Row to parse a `RoomTypeDTO` from.

        Returns:
            A `RoomTypeDTO` parsed from the given row.
        """
        return RoomTypeDTO(id=row[0], name=row[1])
