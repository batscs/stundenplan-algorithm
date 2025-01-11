import logging
from sqlite3 import Row
from typing import final, override

from db.dao.double_key_dao import DoubleKeyDAO
from db.dto.employee_dislikes_date_dto import EmployeeDislikesDateDTO


@final
class EmployeeDislikesDateDAO(DoubleKeyDAO[EmployeeDislikesDateDTO]):
    """Represents a Data Access Object (DAO) for managing objects of type `EmployeeDislikesDateDTO`.

    It is implemented as a singleton, meaning that only one instance of this class exists at
    runtime. Note that this class is not thread-safe in any way.
    """

    @override
    def __init__(self) -> None:
        """Initializes an `EmployeeDislikesDateDAO`.

        It additionally creates the corresponding database table if it does not exist yet.

        Note that this method will only initialize the one and only instance at runtime of the
        `EmployeeDislikesDateDAO` class. All calls to this method afterwards are guaranteed to have
        no effect.
        """
        super().__init__(
            logger=logging.getLogger(__name__),
            table_name="employee_dislikes_date",
            create_table_query="""
                CREATE TABLE IF NOT EXISTS employee_dislikes_date (
                    employee_id INTEGER NOT NULL REFERENCES employee(id) ON UPDATE CASCADE ON DELETE CASCADE, 
                    date_id INTEGER NOT NULL REFERENCES date(id) ON UPDATE CASCADE ON DELETE CASCADE,
                    priority_id INTEGER NOT NULL REFERENCES priority(id) ON UPDATE CASCADE ON DELETE CASCADE,
                    PRIMARY KEY (employee_id, date_id)
                );
                """,
            insert_query="""
                INSERT INTO employee_dislikes_date (employee_id, date_id, priority_id)
                VALUES (:employee_id, :date_id, :priority_id);
                """,
            select_query="""
                SELECT employee_id, date_id, priority_id
                FROM employee_dislikes_date
                WHERE employee_id = :first_id AND date_id = :second_id;
                """,
            select_all_query="""
                SELECT employee_id, date_id, priority_id
                FROM employee_dislikes_date;
                """,
            update_query="""
                UPDATE employee_dislikes_date
                SET priority_id = :priority_id
                WHERE employee_id = :employee_id AND date_id = :date_id;
                """,
            delete_query="""
                DELETE FROM employee_dislikes_date
                WHERE employee_id = :first_id AND date_id = :second_id;
                """,
        )

    @override
    def _parse_row(self, row: Row) -> EmployeeDislikesDateDTO:
        """Parses an `EmployeeDislikesDateDTO` from a given row.

        Args:
            row: Row to parse an `EmployeeDislikesDateDTO` from.

        Returns:
            An `EmployeeDislikesDateDTO` parsed from the given row.
        """
        return EmployeeDislikesDateDTO(
            employee_id=row[0],
            date_id=row[1],
            priority_id=row[2],
        )
