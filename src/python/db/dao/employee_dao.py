import logging
from sqlite3 import Row
from typing import final, override

from db.dao.single_key_dao import SingleKeyDAO
from db.dto.employee_dto import EmployeeDTO


@final
class EmployeeDAO(SingleKeyDAO[EmployeeDTO]):
    """Represents a Data Access Object (DAO) for managing objects of type `EmployeeDTO`.

    It is implemented as a singleton, meaning that only one instance of this class exists at
    runtime. Note that this class is not thread-safe in any way.
    """

    @override
    def __init__(self) -> None:
        """Initializes an `EmployeeDAO`.

        It additionally creates the corresponding database table if it does not exist yet.

        Note that this method will only initialize the one and only instance at runtime of the
        `EmployeeDAO` class. All calls to this method afterwards are guaranteed to have no effect.
        """
        super().__init__(
            logger=logging.getLogger(__name__),
            table_name="employee",
            create_table_query="""
                CREATE TABLE IF NOT EXISTS employee (
                    id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    abbreviation TEXT NOT NULL UNIQUE, 
                    title TEXT, 
                    first_name TEXT NOT NULL, 
                    last_name TEXT NOT NULL,
                    employee_type_id INTEGER NOT NULL REFERENCES employee_type(id) ON UPDATE CASCADE ON DELETE CASCADE
                );
                """,
            insert_query="""
                INSERT INTO employee (abbreviation, title, first_name, last_name, employee_type_id)
                VALUES (:abbreviation, :title, :first_name, :last_name, :employee_type_id);
                """,
            select_query="""
                SELECT id, abbreviation, title, first_name, last_name, employee_type_id
                FROM employee
                WHERE id = :id;
                """,
            select_all_query="""
                SELECT id, abbreviation, title, first_name, last_name, employee_type_id
                FROM employee;
                """,
            update_query="""
                UPDATE employee
                SET abbreviation = :abbreviation, title = :title, first_name = :first_name, last_name = :last_name, employee_type_id = :employee_type_id
                WHERE id = :id;
                """,
            delete_query="""
                DELETE
                FROM employee
                WHERE id = :id;
                """,
        )

    @override
    def _parse_row(self, row: Row) -> EmployeeDTO:
        """Parses an `EmployeeDTO` from a given row.

        Args:
            row: Row to parse an `EmployeeDTO` from.

        Returns:
            An `EmployeeDTO` parsed from the given row.
        """
        return EmployeeDTO(
            id=row[0],
            abbreviation=row[1],
            title=row[2],
            first_name=row[3],
            last_name=row[4],
            employee_type_id=row[5],
        )
