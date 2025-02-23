from app.config.postgres_orm_config import scoped_session_factory
from app.v1.entity.BehaviorRecords import BehaviorRecords
from app.config.logger_config import LogConfig

# Set up a logger for this repository
logger = LogConfig.setup_logger(__name__)

class BehaviorRecordsRepository:
    def __init__(self, scoped_session_factory):
        self.scoped_session_factory = scoped_session_factory

    def get_record_by_id(self, record_id):
        """Retrieve a behavior record by its ID."""
        session = self.scoped_session_factory()
        try:
            logger.info(f"Fetching behavior record with ID: {record_id}")
            return session.query(BehaviorRecords).filter(BehaviorRecords.id == record_id).one_or_none()
        finally:
            session.close()

    def get_records_by_student_id(self, student_id):
        """Retrieve behavior records by student ID."""
        session = self.scoped_session_factory()
        try:
            logger.info(f"Fetching behavior records for student ID: {student_id}")
            return session.query(BehaviorRecords).filter(BehaviorRecords.student_id == student_id).all()
        finally:
            session.close()

    def create_record(self, record_data):
        """Create a new behavior record."""
        session = self.scoped_session_factory()
        try:
            record = BehaviorRecords(**record_data)
            session.add(record)
            session.commit()
            logger.info(f"Created behavior record for student ID: {record.student_id}")
            return record
        except Exception as e:
            session.rollback()
            logger.error(f"Error creating behavior record: {e}")
            raise e
        finally:
            session.close()

    def update_record(self, record_id, record_data):
        """Update an existing behavior record."""
        session = self.scoped_session_factory()
        try:
            record = session.query(BehaviorRecords).filter(BehaviorRecords.id == record_id).one_or_none()
            if record:
                for key, value in record_data.items():
                    setattr(record, key, value)
                session.commit()
                logger.info(f"Updated behavior record with ID: {record_id}")
                return record
            logger.warning(f"Behavior record with ID: {record_id} not found")
            return None
        except Exception as e:
            session.rollback()
            logger.error(f"Error updating behavior record: {e}")
            raise e
        finally:
            session.close()

    def delete_record(self, record_id):
        """Delete a behavior record by its ID."""
        session = self.scoped_session_factory()
        try:
            record = session.query(BehaviorRecords).filter(BehaviorRecords.id == record_id).one_or_none()
            if record:
                session.delete(record)
                session.commit()
                logger.info(f"Deleted behavior record with ID: {record_id}")
                return True
            logger.warning(f"Behavior record with ID: {record_id} not found")
            return False
        except Exception as e:
            session.rollback()
            logger.error(f"Error deleting behavior record: {e}")
            raise e
        finally:
            session.close()
