from app.config.postgres_orm_config import scoped_session_factory
from app.v1.entity.Students import Students
from app.config.logger_config import LogConfig

# Set up a logger for this repository
logger = LogConfig.setup_logger(__name__)

class StudentsRepository:
    def __init__(self, scoped_session_factory):
        self.scoped_session_factory = scoped_session_factory

    def get_all_students(self):
        """Retrieve all students."""
        session = self.scoped_session_factory()
        try:
            logger.info("Fetching all students")
            return session.query(Students).all()
        finally:
            session.close()

    def get_students_by_class_and_section(self, class_value, section):
        """Retrieve students by class and section."""
        session = self.scoped_session_factory()
        try:
            logger.info(f"Fetching students for class: {class_value}, section: {section}")
            return session.query(Students).filter(Students.class_value == class_value, Students.section == section).all()
        finally:
            session.close()

    def get_student_by_id(self, student_id):
        """Retrieve a student by their ID."""
        session = self.scoped_session_factory()
        try:
            logger.info(f"Fetching student with ID: {student_id}")
            return session.query(Students).filter(Students.student_id == student_id).one_or_none()
        finally:
            session.close()
