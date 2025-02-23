from app.config.postgres_orm_config import scoped_session_factory
from app.v1.entity.TimeTable import TimeTable
from app.config.logger_config import LogConfig

# Set up a logger for this repository
logger = LogConfig.setup_logger(__name__)

class TimeTableRepository:
    def __init__(self, scoped_session_factory):
        self.scoped_session_factory = scoped_session_factory

    def get_time_table_by_id(self, time_table_id):
        """Retrieve a time table entry by its ID."""
        session = self.scoped_session_factory()
        try:
            logger.info(f"Fetching time table entry with ID: {time_table_id}")
            return session.query(TimeTable).filter(TimeTable.id == time_table_id).one_or_none()
        finally:
            session.close()

    def get_time_table_by_class_and_section(self, class_value, section):
        """Retrieve time table entries by class and section."""
        session = self.scoped_session_factory()
        try:
            logger.info(f"Fetching time table entries for class: {class_value}, section: {section}")
            return session.query(TimeTable).filter(TimeTable.class_value == class_value, TimeTable.section == section).all()
        finally:
            session.close()

    def create_time_table(self, time_table_data):
        """Create a new time table entry."""
        session = self.scoped_session_factory()
        try:
            time_table = TimeTable(**time_table_data)
            session.add(time_table)
            session.commit()
            logger.info(f"Created time table entry with ID: {time_table.id}")
            return time_table
        except Exception as e:
            session.rollback()
            logger.error(f"Error creating time table entry: {e}")
            raise e
        finally:
            session.close()

    def update_time_table(self, time_table_id, time_table_data):
        """Update an existing time table entry."""
        session = self.scoped_session_factory()
        try:
            time_table = session.query(TimeTable).filter(TimeTable.id == time_table_id).one_or_none()
            if time_table:
                for key, value in time_table_data.items():
                    setattr(time_table, key, value)
                session.commit()
                logger.info(f"Updated time table entry with ID: {time_table_id}")
                return time_table
            logger.warning(f"Time table entry with ID: {time_table_id} not found")
            return None
        except Exception as e:
            session.rollback()
            logger.error(f"Error updating time table entry: {e}")
            raise e
        finally:
            session.close()

    def delete_time_table(self, time_table_id):
        """Delete a time table entry by its ID."""
        session = self.scoped_session_factory()
        try:
            time_table = session.query(TimeTable).filter(TimeTable.id == time_table_id).one_or_none()
            if time_table:
                session.delete(time_table)
                session.commit()
                logger.info(f"Deleted time table entry with ID: {time_table_id}")
                return True
            logger.warning(f"Time table entry with ID: {time_table_id} not found")
            return False
        except Exception as e:
            session.rollback()
            logger.error(f"Error deleting time table entry: {e}")
            raise e
        finally:
            session.close()
