from app.config.postgres_orm_config import scoped_session_factory
from app.v1.entity.Users import Users
from app.config.logger_config import LogConfig

# Set up a logger for this controller
logger = LogConfig.setup_logger(__name__)

class UsersRepository:
    def __init__(self, scoped_session_factory):
        self.scoped_session_factory = scoped_session_factory

    def get_user_by_id(self, user_id):
        """Retrieve a user by their ID."""
        session = self.scoped_session_factory()
        try:
            logger.info(f"Fetching user with ID: {user_id}")
            return session.query(Users).filter(Users.id == user_id).one_or_none()
        finally:
            session.close()

    def get_user_by_email(self, email):
        """Retrieve a user by their email."""
        session = self.scoped_session_factory()
        try:
            logger.info(f"Fetching user with email: {email}")
            return session.query(Users).filter(Users.email == email).one_or_none()
        finally:
            session.close()

    def create_user(self, user_data):
        """Create a new user."""
        session = self.scoped_session_factory()
        try:
            user = Users(**user_data)
            session.add(user)
            session.commit()
            logger.info(f"Created user with email: {user.email}")
            return user
        except Exception as e:
            session.rollback()
            logger.error(f"Error creating user: {e}")
            raise e
        finally:
            session.close()

    def update_user(self, user_id, user_data):
        """Update an existing user."""
        session = self.scoped_session_factory()
        try:
            user = session.query(Users).filter(Users.id == user_id).one_or_none()
            if user:
                for key, value in user_data.items():
                    setattr(user, key, value)
                session.commit()
                logger.info(f"Updated user with ID: {user_id}")
                return user
            logger.warning(f"User with ID: {user_id} not found")
            return None
        except Exception as e:
            session.rollback()
            logger.error(f"Error updating user: {e}")
            raise e
        finally:
            session.close()

    def delete_user(self, user_id):
        """Delete a user by their ID."""
        session = self.scoped_session_factory()
        try:
            user = session.query(Users).filter(Users.id == user_id).one_or_none()
            if user:
                session.delete(user)
                session.commit()
                logger.info(f"Deleted user with ID: {user_id}")
                return True
            logger.warning(f"User with ID: {user_id} not found")
            return False
        except Exception as e:
            session.rollback()
            logger.error(f"Error deleting user: {e}")
            raise e
        finally:
            session.close()
