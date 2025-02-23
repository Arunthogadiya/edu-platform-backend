from app.config.postgres_orm_config import scoped_session_factory
from app.v1.entity.Event import Event
from app.config.logger_config import LogConfig
import datetime

# Set up a logger for this repository
logger = LogConfig.setup_logger(__name__)

class EventRepository:
    def __init__(self, scoped_session_factory):
        self.scoped_session_factory = scoped_session_factory

    def create_event(self, event_data):
        """Create a new event."""
        session = self.scoped_session_factory()
        try:
            event = Event(**event_data)
            session.add(event)
            session.commit()
            session.refresh(event)
            logger.info(f"Created event with ID: {event.id}")
            return event
        except Exception as e:
            session.rollback()
            logger.error(f"Error creating event: {e}")
            raise e
        finally:
            session.close()

    def get_upcoming_events(self, class_value, section):
        """Retrieve upcoming events filtered by class value and section."""
        session = self.scoped_session_factory()
        try:
            logger.info(f"Fetching upcoming events for class: {class_value}, section: {section}")
            return session.query(Event).filter(
                Event.event_date >= datetime.datetime.utcnow(),
                Event.class_value == class_value,
                Event.section == section
            ).all()
        finally:
            session.close()

    def get_previous_events(self, class_value, section):
        """Retrieve previous events filtered by class value and section."""
        session = self.scoped_session_factory()
        try:
            logger.info(f"Fetching previous events for class: {class_value}, section: {section}")
            return session.query(Event).filter(
                Event.event_date < datetime.datetime.utcnow(),
                Event.class_value == class_value,
                Event.section == section
            ).all()
        finally:
            session.close()
