from app.config.postgres_orm_config import scoped_session_factory
from app.v1.entity.ChatbotConversations import ChatbotConversations
from app.config.logger_config import LogConfig

# Set up a logger for this repository
logger = LogConfig.setup_logger(__name__)

class ChatbotConversationsRepository:
    def __init__(self, scoped_session_factory):
        self.scoped_session_factory = scoped_session_factory

    def get_conversation_by_id(self, conversation_id):
        """Retrieve a chatbot conversation by its ID."""
        session = self.scoped_session_factory()
        try:
            logger.info(f"Fetching chatbot conversation with ID: {conversation_id}")
            return session.query(ChatbotConversations).filter(ChatbotConversations.id == conversation_id).one_or_none()
        finally:
            session.close()

    def get_conversations_by_user_id(self, user_id):
        """Retrieve chatbot conversations by user ID."""
        session = self.scoped_session_factory()
        try:
            logger.info(f"Fetching chatbot conversations for user ID: {user_id}")
            return session.query(ChatbotConversations).filter(ChatbotConversations.user_id == user_id).all()
        finally:
            session.close()

    def create_conversation(self, conversation_data):
        """Create a new chatbot conversation."""
        session = self.scoped_session_factory()
        try:
            conversation = ChatbotConversations(**conversation_data)
            session.add(conversation)
            session.commit()
            logger.info(f"Created chatbot conversation for user ID: {conversation.user_id}")
            return conversation
        except Exception as e:
            session.rollback()
            logger.error(f"Error creating chatbot conversation: {e}")
            raise e
        finally:
            session.close()

    def update_conversation(self, conversation_id, conversation_data):
        """Update an existing chatbot conversation."""
        session = self.scoped_session_factory()
        try:
            conversation = session.query(ChatbotConversations).filter(ChatbotConversations.id == conversation_id).one_or_none()
            if conversation:
                for key, value in conversation_data.items():
                    setattr(conversation, key, value)
                session.commit()
                logger.info(f"Updated chatbot conversation with ID: {conversation_id}")
                return conversation
            logger.warning(f"Chatbot conversation with ID: {conversation_id} not found")
            return None
        except Exception as e:
            session.rollback()
            logger.error(f"Error updating chatbot conversation: {e}")
            raise e
        finally:
            session.close()

    def delete_conversation(self, conversation_id):
        """Delete a chatbot conversation by its ID."""
        session = self.scoped_session_factory()
        try:
            conversation = session.query(ChatbotConversations).filter(ChatbotConversations.id == conversation_id).one_or_none()
            if conversation:
                session.delete(conversation)
                session.commit()
                logger.info(f"Deleted chatbot conversation with ID: {conversation_id}")
                return True
            logger.warning(f"Chatbot conversation with ID: {conversation_id} not found")
            return False
        except Exception as e:
            session.rollback()
            logger.error(f"Error deleting chatbot conversation: {e}")
            raise e
        finally:
            session.close()
