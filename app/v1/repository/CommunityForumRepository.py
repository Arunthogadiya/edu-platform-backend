from app.config.postgres_orm_config import scoped_session_factory
from app.v1.entity.CommunityForum import CommunityForum
from app.config.logger_config import LogConfig

# Set up a logger for this repository
logger = LogConfig.setup_logger(__name__)

class CommunityForumRepository:
    def __init__(self, scoped_session_factory):
        self.scoped_session_factory = scoped_session_factory

    def get_all_forums(self):
        """Retrieve all forum discussions."""
        session = self.scoped_session_factory()
        try:
            logger.info("Fetching all forum discussions")
            return session.query(CommunityForum).filter(CommunityForum.is_reply == False).all()
        finally:
            session.close()

    def get_replies_by_forum_id(self, forum_id):
        """Retrieve all replies for a specific forum discussion."""
        session = self.scoped_session_factory()
        try:
            logger.info(f"Fetching replies for forum ID: {forum_id}")
            return session.query(CommunityForum).filter(CommunityForum.forum_id == forum_id, CommunityForum.is_reply == True).all()
        finally:
            session.close()

    def create_forum(self, forum_data):
        """Create a new forum discussion."""
        session = self.scoped_session_factory()
        try:
            forum = CommunityForum(**forum_data)
            session.add(forum)
            session.commit()
            logger.info(f"Created forum discussion with ID: {forum.id}")
            return forum
        except Exception as e:
            session.rollback()
            logger.error(f"Error creating forum discussion: {e}")
            raise e
        finally:
            session.close()

    def create_reply(self, reply_data):
        """Create a new reply to a forum discussion."""
        session = self.scoped_session_factory()
        try:
            reply = CommunityForum(**reply_data)
            session.add(reply)
            session.commit()
            logger.info(f"Created reply with ID: {reply.id}")
            return reply
        except Exception as e:
            session.rollback()
            logger.error(f"Error creating reply: {e}")
            raise e
        finally:
            session.close()
