from app.config.postgres_orm_config import scoped_session_factory
from app.v1.entity.Activities import Activities
from app.config.logger_config import LogConfig

# Set up a logger for this repository
logger = LogConfig.setup_logger(__name__)

class ActivitiesRepository:
    def __init__(self, scoped_session_factory):
        self.scoped_session_factory = scoped_session_factory

    def get_activity_by_id(self, activity_id):
        """Retrieve an activity by its ID."""
        session = self.scoped_session_factory()
        try:
            logger.info(f"Fetching activity with ID: {activity_id}")
            return session.query(Activities).filter(Activities.id == activity_id).one_or_none()
        finally:
            session.close()

    def get_activities_by_student_id(self, student_id):
        """Retrieve activities by student ID."""
        session = self.scoped_session_factory()
        try:
            logger.info(f"Fetching activities for student ID: {student_id}")
            return session.query(Activities).filter(Activities.student_id == student_id).all()
        finally:
            session.close()

    def create_activity(self, activity_data):
        """Create a new activity."""
        session = self.scoped_session_factory()
        try:
            activity = Activities(**activity_data)
            session.add(activity)
            session.commit()
            logger.info(f"Created activity for student ID: {activity.student_id}")
            return activity
        except Exception as e:
            session.rollback()
            logger.error(f"Error creating activity: {e}")
            raise e
        finally:
            session.close()

    def update_activity(self, activity_id, activity_data):
        """Update an existing activity."""
        session = self.scoped_session_factory()
        try:
            activity = session.query(Activities).filter(Activities.id == activity_id).one_or_none()
            if activity:
                for key, value in activity_data.items():
                    setattr(activity, key, value)
                session.commit()
                logger.info(f"Updated activity with ID: {activity_id}")
                return activity
            logger.warning(f"Activity with ID: {activity_id} not found")
            return None
        except Exception as e:
            session.rollback()
            logger.error(f"Error updating activity: {e}")
            raise e
        finally:
            session.close()

    def delete_activity(self, activity_id):
        """Delete an activity by its ID."""
        session = self.scoped_session_factory()
        try:
            activity = session.query(Activities).filter(Activities.id == activity_id).one_or_none()
            if activity:
                session.delete(activity)
                session.commit()
                logger.info(f"Deleted activity with ID: {activity_id}")
                return True
            logger.warning(f"Activity with ID: {activity_id} not found")
            return False
        except Exception as e:
            session.rollback()
            logger.error(f"Error deleting activity: {e}")
            raise e
        finally:
            session.close()
