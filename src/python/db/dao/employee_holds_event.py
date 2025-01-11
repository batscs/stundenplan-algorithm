import logging
from sqlite3 import Row
from typing import final, override

from db.dao.double_key_dao import DoubleKeyDAO
from db.dto.employee_holds_event_dto import EmployeeHoldsEventDTO


@final
class EmployeeHoldsEventDAO(DoubleKeyDAO[EmployeeHoldsEventDTO]):
    """Represents a Data Access Object (DAO) for managing objects of type `EmployeeHoldsEventDTO`.

    It is implemented as a singleton, meaning that only one instance of this class exists at
    runtime. Note that this class is not thread-safe in any way.
    """

    @override
    def __init__(self) -> None:
        """Initializes an `EmployeeHoldsEventDAO`.

        It additionally creates the corresponding database table if it does not exist yet.

        Note that this method will only initialize the one and only instance at runtime of the
        `EmployeeHoldsEventDAO` class. All calls to this method afterwards are guaranteed to have no
        effect.
        """
        super().__init__(
            logger=logging.getLogger(__name__),
            table_name="employee_holds_event",
            create_table_query="""
               CREATE TABLE IF NOT EXISTS employee_holds_event (
                   employee_id INTEGER NOT NULL REFERENCES employee(id) ON UPDATE CASCADE ON DELETE CASCADE, 
                   event_id INTEGER NOT NULL REFERENCES event(id) ON UPDATE CASCADE ON DELETE CASCADE,
                   PRIMARY KEY (employee_id, event_id)
               );
               """,
            insert_query="""
               INSERT INTO employee_holds_event (employee_id, event_id)
               VALUES (:employee_id, :event_id);
               """,
            select_query="""
               SELECT employee_id, event_id
               FROM employee_holds_event
               WHERE employee_id = :first_id AND event_id = :second_id;
               """,
            select_all_query="""
               SELECT employee_id, event_id
               FROM employee_holds_event;
               """,
            update_query="""
               UPDATE employee_holds_event
               SET employee_id = :employee_id, event_id = :event_id 
               WHERE employee_id = :employee_id AND event_id = :event_id;
               """,
            delete_query="""
               DELETE FROM employee_holds_event
               WHERE employee_id = :first_id AND event_id = :second_id;
               """,
        )

    @override
    def _parse_row(self, row: Row) -> EmployeeHoldsEventDTO:
        """Parses an `EmployeeHoldsEventDTO` from a given row.

        Args:
            row: Row to parse an `EmployeeHoldsEventDTO` from.

        Returns:
            An `EmployeeHoldsEventDTO` parsed from the given row.
        """
        return EmployeeHoldsEventDTO(employee_id=row[0], event_id=row[1])
