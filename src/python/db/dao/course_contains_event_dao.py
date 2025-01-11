import logging
from sqlite3 import Row
from typing import final, override

from db.dao.triple_key_dao import TripleKeyDAO
from db.dto.course_contains_event_dto import CourseContainsEventDTO


@final
class CourseContainsEventDAO(TripleKeyDAO[CourseContainsEventDTO]):
    """Represents a Data Access Object (DAO) for managing objects of type `CourseContainsEventDTO`.

    It is implemented as a singleton, meaning that only one instance of this class exists at
    runtime. Note that this class is not thread-safe in any way.
    """

    @override
    def __init__(self) -> None:
        """Initializes a `CourseContainsEventDAO`.

        It additionally creates the corresponding database table if it does not exist yet.

        Note that this method will only initialize the one and only instance at runtime of the
        `CourseContainsEventDAO` class. All calls to this method afterwards are guaranteed to have
        no effect.
        """
        super().__init__(
            logger=logging.getLogger(__name__),
            table_name="course_contains_event",
            create_table_query="""
                CREATE TABLE IF NOT EXISTS course_contains_event (                    
                    course_id INTEGER NOT NULL REFERENCES course(id) ON UPDATE CASCADE ON DELETE CASCADE,
                    semester_id INTEGER NOT NULL REFERENCES semester(id) ON UPDATE CASCADE ON DELETE CASCADE,
                    event_id INTEGER NOT NULL REFERENCES event(id) ON UPDATE CASCADE ON DELETE CASCADE,
                    PRIMARY KEY (course_id, semester_id, event_id)
                );
                """,
            insert_query="""
                INSERT INTO course_contains_event (course_id, semester_id, event_id)
                VALUES (:course_id, :semester_id, :event_id);
                """,
            select_query="""
                SELECT course_id, semester_id, event_id
                FROM course_contains_event
                WHERE course_id = :first_id AND semester_id = :second_id AND event_id = :third_id;
                """,
            select_all_query="""
                SELECT course_id, semester_id, event_id
                FROM course_contains_event;
                """,
            update_query="""
                UPDATE course_contains_event
                SET course_id = :course_id, semester_id = :semester_id, event_id = :event_id
                WHERE course_id = :first_id AND semester_id = :second_id AND event_id = :third_id;
                """,
            delete_query="""
                DELETE
                FROM course_contains_event
                WHERE course_id = :first_id AND semester_id = :second_id AND event_id = :third_id;
                """,
        )

    @override
    def _parse_row(self, row: Row) -> CourseContainsEventDTO:
        """Parses a `CourseContainsEventDTO` from a given row.

        Args:
            row: Row to parse a `CourseContainsEventDTO` from.

        Returns:
            A `CourseContainsEventDTO` parsed from the given row.
        """
        return CourseContainsEventDTO(
            course_id=row[0], semester_id=row[1], event_id=row[2]
        )
