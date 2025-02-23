from app.config.postgres_orm_config import scoped_session_factory
from app.v1.entity.Assessment import Assessment
from app.config.logger_config import LogConfig
import datetime

# Set up a logger for this repository
logger = LogConfig.setup_logger(__name__)

class AssessmentRepository:
    def __init__(self, scoped_session_factory):
        self.scoped_session_factory = scoped_session_factory

    def create_assessment(self, assessment_data):
        """Create a new assessment."""
        session = self.scoped_session_factory()
        try:
            assessment = Assessment(**assessment_data)
            session.add(assessment)
            session.commit()
            session.refresh(assessment)
            logger.info(f"Created assessment with ID: {assessment.id}")
            return assessment
        except Exception as e:
            session.rollback()
            logger.error(f"Error creating assessment: {e}")
            raise e
        finally:
            session.close()

    def get_upcoming_assessments(self, class_value, section):
        """Retrieve upcoming assessments filtered by class value and section."""
        session = self.scoped_session_factory()
        try:
            logger.info(f"Fetching upcoming assessments for class: {class_value}, section: {section}")
            return session.query(Assessment).filter(
                Assessment.assessment_date >= datetime.datetime.utcnow(),
                Assessment.class_value == class_value,
                Assessment.section == section
            ).all()
        finally:
            session.close()

    def get_previous_assessments(self, class_value, section):
        """Retrieve previous assessments filtered by class value and section."""
        session = self.scoped_session_factory()
        try:
            logger.info(f"Fetching previous assessments for class: {class_value}, section: {section}")
            return session.query(Assessment).filter(
                Assessment.assessment_date < datetime.datetime.utcnow(),
                Assessment.class_value == class_value,
                Assessment.section == section
            ).all()
        finally:
            session.close()
