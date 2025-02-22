from app.config.postgres_orm_config import scoped_session_factory
from app.v1.entity.CommunityPoll import CommunityPoll
from app.config.logger_config import LogConfig

# Set up a logger for this repository
logger = LogConfig.setup_logger(__name__)

class CommunityPollRepository:
    def __init__(self, scoped_session_factory):
        self.scoped_session_factory = scoped_session_factory

    def get_all_polls(self):
        """Retrieve all active polls."""
        session = self.scoped_session_factory()
        try:
            logger.info("Fetching all active polls")
            return session.query(CommunityPoll).all()
        finally:
            session.close()

    def create_poll(self, poll_data):
        """Create a new poll."""
        session = self.scoped_session_factory()
        try:
            poll = CommunityPoll(**poll_data)
            session.add(poll)
            session.commit()
            session.refresh(poll)  # Ensure the poll instance is bound to the session
            logger.info(f"Created poll with ID: {poll.id}")
            return poll
        except Exception as e:
            session.rollback()
            logger.error(f"Error creating poll: {e}")
            raise e
        finally:
            session.close()

    def update_poll_votes(self, poll_id, votes):
        """Update votes for a poll."""
        session = self.scoped_session_factory()
        try:
            poll = session.query(CommunityPoll).filter(CommunityPoll.id == poll_id).one_or_none()
            if poll:
                poll.votes = votes
                session.commit()
                logger.info(f"Updated votes for poll with ID: {poll_id}")
                return None
            logger.warning(f"Poll with ID: {poll_id} not found")
            return None
        except Exception as e:
            session.rollback()
            logger.error(f"Error updating poll votes: {e}")
            raise e
        finally:
            session.close()

    def get_poll_by_id(self, poll_id):
        """Retrieve a poll by its ID."""
        session = self.scoped_session_factory()
        try:
            logger.info(f"Fetching poll with ID: {poll_id}")
            return session.query(CommunityPoll).filter(CommunityPoll.id == poll_id).one_or_none()
        finally:
            session.close()
