import atexit
import logging
import os
import sqlite3
from logging import Logger
from sqlite3 import Connection, Error
from contextlib import contextmanager
from datetime import time
from queue import Queue
from typing import Any, Generator, Optional, Self, final

from utils import path_utils, time_utils


@final
class Database:
    """Represents the `Database` of the time schedule generator.

    It is implemented as a singleton, meaning that only one actual instance exists at runtime.
    This class is not thread-safe and intended not to be inherited from.
    """

    DB_FILE_NAME: str = "FHW.db"
    """Name of the internal database file."""

    DB_FILE_PATH: str = os.path.join(path_utils.RESOURCES_PATH, DB_FILE_NAME)
    "Path to the internal database file."

    MAX_CONNECTIONS: int = 4
    "Maximum pooled connections to the database."

    __instance: Optional[Self] = None
    """Single instance of this `Database` at runtime."""

    __is_initialized: bool = False
    """Whether the single instance of this `Database` is initialized."""

    def __new__(cls) -> Self:
        """Constructs a new `Database` instance if none exists yet.

        Returns:
            A new `Database` instance if none exists yet, otherwise the existing one.
        """
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __delete_database_file(self) -> None:
        """Deletes the database file if it exists.

        This function must only be called if no connections exist to the database, i. e. before
        a call to `__initialize_connection_pool` or after a call to `__clean_connection_pool`.

        Raises:
            `RuntimeError`: If a connection pool already exists.
        """
        if self.__connection_pool is not None:
            error: RuntimeError = RuntimeError(
                "Cannot delete database file, a connection pool already exists."
            )
            self.__logger.exception(error)
            raise error
        self.__logger.debug(
            f"Deleting database file {self.__class__.DB_FILE_NAME} if it exists"
        )
        if os.path.exists(self.__class__.DB_FILE_PATH):
            os.remove(self.__class__.DB_FILE_PATH)
            self.__logger.debug(f"Deleted database file {self.__class__.DB_FILE_NAME}")
        else:
            self.__logger.debug(
                f"Database file {self.__class__.DB_FILE_NAME} did not exist"
            )

    def __initialize_connection_pool(self) -> None:
        """Initializes the connection pool by creating a certain number of connections to the
        database.

        Note that this method must only be called if no connection pool exists yet, i. e. at the
        start or after a call to `__clean_connection_pool`.

        Raises:
            `RuntimeError`: If a connection pool already exists.
            `sqlite3.Error`: If any error occurs while creating the connections.
        """
        if self.__connection_pool is not None:
            error: Exception = RuntimeError("A connection pool already exists.")
            self.__logger.exception(error)
            raise error
        try:
            self.__connection_pool = Queue(maxsize=self.__class__.MAX_CONNECTIONS)
            for i in range(self.__class__.MAX_CONNECTIONS):
                self.__logger.debug(f"Creating connection {i}")
                connection: Connection = sqlite3.connect(
                    database=self.__class__.DB_FILE_PATH,
                    detect_types=sqlite3.PARSE_DECLTYPES,
                    autocommit=True,
                )
                self.__connection_pool.put(connection)
                self.__logger.debug(f"Created connection {i}: {connection}")
        except Error as error:
            self.__logger.exception(error)
            raise

    def __clean_connection_pool(self) -> None:
        """Cleans the connection pool by closing all existing connections to the database.

        Note that this method must only be called if a connection pool exists and after all
        connections have been returned.

        Raises:
            `RuntimeError`: If no connection pool exists or not all connections have been returned.
        """
        if self.__connection_pool is None:
            error: Exception = RuntimeError("No connection pool exists.")
            self.__logger.exception(error)
            raise error
        if self.__connection_pool.qsize() < self.__class__.MAX_CONNECTIONS:
            error: Exception = RuntimeError(
                f"Not all connections have been returned to the connection pool. "
                + f"Expected {self.__class__.MAX_CONNECTIONS} connections in the pool, "
                + f"but it only has {self.__connection_pool.qsize()}."
            )
            self.__logger.exception(error)
            raise error
        # Queue does not implement Iterable[T], so we can't use enumerate and have to increment
        # the index ourselves.
        i: int = 0
        while self.__connection_pool.qsize() > 0:
            connection: Connection = self.__connection_pool.get()
            self.__logger.debug(f"Closing connection {i}: {connection}")
            connection.close()
            self.__logger.debug(f"Closed connection {i}")
            i += 1

    def initialize(self, delete_database_file: bool = False) -> None:
        """Initializes the one and only `Database` instance at runtime.

        Note that the `Database` can only be initialized once, meaning that every call to this
        method after the first one is guaranteed to have no effect.

        Args:
            delete_database_file: Whether the database file should be deleted or not, `False` by
                default.

        Raises:
            `sqlite3.Error`: If any error occurs while initializing the database.
        """
        if self.__class__.__is_initialized:
            return
        self.__class__.__is_initialized = True
        self.__logger: Logger = logging.getLogger(__name__)
        self.__connection_pool: Optional[Queue[Connection]] = None
        # We use the named style, which avoids issues with the order and count of query parameters.
        sqlite3.paramstyle = "named"
        # SQLite3 does not support time objects, so we need to convert them to a custom "TIME" type,
        # which is effectively stored as an integer (number of minutes since midnight).
        sqlite3.register_adapter(time, time_utils.time_to_minutes)
        sqlite3.register_converter("TIME", lambda s: time_utils.minutes_to_time(int(s)))
        if delete_database_file:
            self.__delete_database_file()
        self.__initialize_connection_pool()
        # Make sure to be nice and close all existing connections on exit.
        atexit.register(self.__clean_connection_pool)

    @contextmanager
    def create_connection(
        self, block: bool = True, timeout: Optional[float] = None
    ) -> Generator[Connection, Any, None]:
        """Creates a `Connection` to the database.

        Note that the yielded `Connection` originates from a connection pool, to which it is
        automatically returned. It must not be closed manually.

        Args:
            block: Whether the call should block until a connection becomes available, `True` by
                default.
            timeout: Optional timeout in seconds for waiting, `None` by default.

        Returns:
            A `Connection` to the database.

        Raises:
            `RuntimeError`: If no connection pool exists.
            `Empty`: If `block` is `True`, `timeout` is specified and no connection becomes
                available within the given timeout. Also raised if `block` is `False` and no
                connection is immediately available (`timeout` is ignored in that case).
        """
        if self.__connection_pool is None:
            error: RuntimeError = RuntimeError("No connection pool exists.")
            self.__logger.exception(error)
            raise error
        try:
            connection: Connection = self.__connection_pool.get(block, timeout)
            # This really clogs up the log file, so only enable for debugging if necessary.
            # self.__logger.debug(f"Yielding connection {connection}")
            yield connection
        finally:
            self.__connection_pool.put(connection)
            # self.__logger.debug(f"Returned connection {connection}")
