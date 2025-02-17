from app.config.postgres_orm_config import scoped_session_factory
from app.v1.entity.Notifications import Notifications
from app.config.logger_config import LogConfig

# Set up a logger for this repository
logger = LogConfig.setup_logger(__name__)

class NotificationsRepository:
    def __init__(self, scoped_session_factory):
        self.scoped_session_factory = scoped_session_factory

    def get_notification_by_id(self, notification_id):
        """Retrieve a notification by its ID."""
        session = self.scoped_session_factory()
        try:
            logger.info(f"Fetching notification with ID: {notification_id}")
            return session.query(Notifications).filter(Notifications.id == notification_id).one_or_none()
        finally:
            session.close()

    def get_notifications_by_user_id(self, user_id):
        """Retrieve notifications by user ID."""
        session = self.scoped_session_factory()
        try:
            logger.info(f"Fetching notifications for user ID: {user_id}")
            return session.query(Notifications).filter(Notifications.user_id == user_id).all()
        finally:
            session.close()

    def create_notification(self, notification_data):
        """Create a new notification."""
        session = self.scoped_session_factory()
        try:
            notification = Notifications(**notification_data)
            session.add(notification)
            session.commit()
            logger.info(f"Created notification for user ID: {notification.user_id}")
            return notification
        except Exception as e:
            session.rollback()
            logger.error(f"Error creating notification: {e}")
            raise e
        finally:
            session.close()

    def update_notification(self, notification_id, notification_data):
        """Update an existing notification."""
        session = self.scoped_session_factory()
        try:
            notification = session.query(Notifications).filter(Notifications.id == notification_id).one_or_none()
            if notification:
                for key, value in notification_data.items():
                    setattr(notification, key, value)
                session.commit()
                logger.info(f"Updated notification with ID: {notification_id}")
                return notification
            logger.warning(f"Notification with ID: {notification_id} not found")
            return None
        except Exception as e:
            session.rollback()
            logger.error(f"Error updating notification: {e}")
            raise e
        finally:
            session.close()

    def delete_notification(self, notification_id):
        """Delete a notification by its ID."""
        session = self.scoped_session_factory()
        try:
            notification = session.query(Notifications).filter(Notifications.id == notification_id).one_or_none()
            if notification:
                session.delete(notification)
                session.commit()
                logger.info(f"Deleted notification with ID: {notification_id}")
                return True
            logger.warning(f"Notification with ID: {notification_id} not found")
            return False
        except Exception as e:
            session.rollback()
            logger.error(f"Error deleting notification: {e}")
            raise e
        finally:
            session.close()
