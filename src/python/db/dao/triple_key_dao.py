from abc import ABC, abstractmethod
from logging import Logger
from typing import Optional, Self
from sqlite3 import Error, OperationalError, Row

from db.database import Database


class TripleKeyDAO[T](ABC):
    """Represents a Data Access Object (DAO) that abstracts away database tables with a compound
    primary key (made up of three individual ones).

    This class is intended as an abstract base class and must be inherited from by specific DAOs.
    It is implemented as a singleton, meaning that only one instance of each subclass exists at
    runtime. Note that this class is not thread-safe in any way.

    The generic type variable `T` represents the type of Data Transfer Object (DTO) this
    `TripleKeyDAO` is supposed to manage.
    """

    __instance: Optional[Self] = None
    """Single instance at runtime of the subclass inheriting from this `TripleKeyDAO`."""

    __is_initialized: bool = False
    """Whether the single instance is initialized or not."""

    def __new__(cls) -> Self:
        """Constructs a new `TripleKeyDAO` instance if none exists yet.

        Returns:
            A new `TripleKeyDAO` instance if none exists yet, otherwise the existing one.
        """
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(
        self,
        logger: Logger,
        table_name: str,
        create_table_query: str,
        insert_query: str,
        select_query: str,
        select_all_query: str,
        update_query: str,
        delete_query: str,
    ) -> None:
        """Initializes a `TripleKeyDAO` with all necessary information.

        It additionally creates the corresponding database table if it does not exist yet.

        Note that this method will only initialize the one and only instance at runtime of the
        subclass inheriting from this `TripleKeyDAO`. All calls to this method afterwards are
        guaranteed to have no effect.

        Args:
            logger: A `Logger` for logging messages.
            table_name: Name of the database table.
            create_table_query: SQL query to create the database table.
            insert_query: SQL query for inserting an entity in the database table.
            select_query: SQL query for selecting an entity in the database table.
            select_all_query: SQL query for selecting all entities in the database table.
            update_query: SQL query for updating an entity in the database table.
            delete_query: SQL query for deleting an entity in the database table.
        """
        # Avoid initializing the one and only instance at runtime more than once.
        if self.__class__.__is_initialized:
            return
        self.__class__.__is_initialized = True
        super().__init__()
        self.__logger: Logger = logger
        self.__table_name: str = table_name
        self.__create_table_query: str = create_table_query
        self.__insert_query: str = insert_query
        self.__select_query: str = select_query
        self.__select_all_query: str = select_all_query
        self.__update_query: str = update_query
        self.__delete_query: str = delete_query
        self.create_table()

    def create_table(self) -> None:
        """Creates the corresponding database table if it does not exist yet.

        Raises:
            `sqlite3.Error`: If any error occurs while creating the database table.
        """
        self.__logger.debug(
            f"Creating database table {self.__table_name} if it does not exist yet"
        )
        try:
            with Database().create_connection() as connection:
                connection.execute(self.__create_table_query)
            self.__logger.debug(f"Database table {self.__table_name} now exists")
        except Error as error:
            self.__logger.exception(error)
            raise

    def insert(self, entity: T) -> None:
        """Inserts a given entity into the database table.

        Args:
            entity: Entity to insert.

        Raises:
            `sqlite3.Error`: If any error occurs while inserting the entity.
        """
        self.__logger.debug(f"Inserting {self.__table_name}: {entity}")
        try:
            with Database().create_connection() as connection:
                created: bool = (
                    connection.execute(self.__insert_query, entity.__dict__).rowcount
                    > 0
                )
            if created:
                self.__logger.debug(f"Inserted {self.__table_name}: {entity}")
            else:
                raise OperationalError(
                    f"Failed to insert {self.__table_name}: {entity}"
                )
        except Error as error:
            self.__logger.exception(error)
            raise

    def insert_all(self, entities: list[T]) -> None:
        """Inserts multiple entities in a given list into the database table.

        Args:
            entities: List of entities to insert.

        Raises:
            `sqlite3.Error`: If any error occurs while inserting the entities.
        """
        count: int = len(entities)
        self.__logger.debug(f"Inserting {count} {self.__table_name}(s)")
        try:
            with Database().create_connection() as connection:
                connection.execute("BEGIN TRANSACTION;")
                rowcount: int = connection.executemany(
                    self.__insert_query, [entity.__dict__ for entity in entities]
                ).rowcount
                connection.execute("COMMIT;")
            if rowcount == count:
                self.__logger.debug(f"Inserted {count} {self.__table_name}(s)")
            else:
                raise OperationalError(
                    f"Failed to insert {count} {self.__table_name}(s)"
                )
        except Error as error:
            self.__logger.exception(error)
            raise

    @abstractmethod
    def _parse_row(self, row: Row) -> T:
        """Parses an entity from a given row.

        This method is abstract and must be overridden by any specific DAO inheriting from
        this `TripleKeyDAO`.

        Args:
            row: Row to parse an entity from.

        Returns:
            An entity parsed from the given row.
        """
        raise NotImplementedError("Must be overridden by specific DAOs.")

    def select(self, first_id: int, second_id: int, third_id: int) -> T:
        """Selects an entity with three given ids from the database table.

        Args:
            first_id: First id of the entity to select.
            second_id: Second id of the entity to select.
            third_id: Third id of the entity to select.

        Raises:
            `sqlite3.Error`: If any error occurs while selecting the entity.
        """
        self.__logger.debug(
            f"Selecting {self.__table_name} with ids {first_id}, {second_id}, {third_id}"
        )
        try:
            with Database().create_connection() as connection:
                row: Optional[Row] = connection.execute(
                    self.__select_query,
                    {
                        "first_id": first_id,
                        "second_id": second_id,
                        "third_id": third_id,
                    },
                ).fetchone()
            if row:
                entity: T = self._parse_row(row)
                self.__logger.debug(
                    f"Selected {self.__table_name} with ids {first_id}, {second_id}, {third_id}: {entity}"
                )
                return entity
            raise OperationalError(
                f"Failed to select {self.__table_name} with ids {first_id}, {second_id}, {third_id}"
            )
        except Error as error:
            self.__logger.exception(error)
            raise

    def select_all(self) -> list[T]:
        """Selects all entities from the database table.

        Returns:
            All selected entities.

        Raises:
            `sqlite3.Error`: If any error occurs while selecting all entities.
        """
        self.__logger.debug(f"Selecting all {self.__table_name}s")
        try:
            with Database().create_connection() as connection:
                rows: list[Row] = connection.execute(self.__select_all_query).fetchall()
            entities: list[T] = [self._parse_row(row) for row in rows]
            self.__logger.debug(f"Selected {len(entities)} {self.__table_name}(s)")
            return entities
        except Error as error:
            self.__logger.exception(error)
            raise

    def update(self, entity: T) -> None:
        """Updates a given entity in the database table.

        Args:
            entity: Entity to update.

        Raises:
            `sqlite3.Error`: If any error occurs while updating the entity.
        """
        self.__logger.debug(f"Updating {self.__table_name}: {entity}")
        try:
            with Database().create_connection() as connection:
                updated: bool = (
                    connection.execute(self.__update_query, entity.__dict__).rowcount
                ) > 0
            if updated:
                self.__logger.debug(f"Updated {self.__table_name}: {entity}")
            else:
                raise OperationalError(
                    f"Failed to update {self.__table_name}: {entity}, no such entity exists"
                )
        except Error as error:
            self.__logger.exception(error)
            raise

    def delete(self, first_id: int, second_id: int, third_id: int) -> None:
        """Deletes an entity with three given ids from the database table.

        Attributes:
            first_id: First id of the entity to delete.
            second_id: Second id of the entity to delete.
            third_id: Third id of the entity to delete.

        Raises:
            `sqlite3.Error`: If any error occurs while deleting the entity.
        """
        self.__logger.debug(
            f"Deleting {self.__table_name} with ids {first_id}, {second_id}, {third_id}"
        )
        try:
            with Database().create_connection() as connection:
                deleted: bool = (
                    connection.execute(
                        self.__delete_query,
                        {
                            "first_id": first_id,
                            "second_id": second_id,
                            "third_id": third_id,
                        },
                    ).rowcount
                    > 0
                )
            if deleted:
                self.__logger.debug(
                    f"Deleted {self.__table_name} with ids {first_id}, {second_id}, {third_id}"
                )
            else:
                raise OperationalError(
                    f"Failed to delete {self.__table_name} with ids {first_id}, {second_id}, {third_id}, "
                    + "no such entity exists"
                )
        except Error as error:
            self.__logger.exception(error)
            raise
