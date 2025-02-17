from app.config.postgres_orm_config import scoped_session_factory
from app.v1.entity.ParentTeacherChat import ParentTeacherChat
from app.config.logger_config import LogConfig

# Set up a logger for this repository
logger = LogConfig.setup_logger(__name__)

class ParentTeacherChatRepository:
    def __init__(self, scoped_session_factory):
        self.scoped_session_factory = scoped_session_factory

    def get_chat_by_id(self, chat_id):
        """Retrieve a chat message by its ID."""
        session = self.scoped_session_factory()
        try:
            logger.info(f"Fetching chat message with ID: {chat_id}")
            return session.query(ParentTeacherChat).filter(ParentTeacherChat.chat_id == chat_id).one_or_none()
        finally:
            session.close()

    def get_chats_by_teacher_id(self, teacher_id):
        """Retrieve chat messages by teacher ID."""
        session = self.scoped_session_factory()
        try:
            logger.info(f"Fetching chat messages for teacher ID: {teacher_id}")
            return session.query(ParentTeacherChat).filter(ParentTeacherChat.teacher_id == teacher_id).all()
        finally:
            session.close()

    def get_chats_by_parent_id(self, parent_id):
        """Retrieve chat messages by parent ID."""
        session = self.scoped_session_factory()
        try:
            logger.info(f"Fetching chat messages for parent ID: {parent_id}")
            return session.query(ParentTeacherChat).filter(ParentTeacherChat.parent_id == parent_id).all()
        finally:
            session.close()

    def get_chats_by_teacher_id_parent_id(self, teacher_id, parent_id):
        """Retrieve chat messages by both teacher ID and parent ID."""
        session = self.scoped_session_factory()
        try:
            logger.info(f"Fetching chat messages for teacher ID: {teacher_id} and parent ID: {parent_id}")
            return session.query(ParentTeacherChat).filter(
                ParentTeacherChat.teacher_id == teacher_id,
                ParentTeacherChat.parent_id == parent_id
            ).all()
        finally:
            session.close()

    def create_chat(self, chat_data):
        """Create a new chat message."""
        session = self.scoped_session_factory()
        try:
            chat = ParentTeacherChat(**chat_data)
            session.add(chat)
            session.commit()
            logger.info(f"Created chat message from {chat.sender} with ID: {chat.chat_id}")
            return chat
        except Exception as e:
            session.rollback()
            logger.error(f"Error creating chat message: {e}")
            raise e
        finally:
            session.close()

    def update_chat(self, chat_id, chat_data):
        """Update an existing chat message."""
        session = self.scoped_session_factory()
        try:
            chat = session.query(ParentTeacherChat).filter(ParentTeacherChat.chat_id == chat_id).one_or_none()
            if chat:
                for key, value in chat_data.items():
                    setattr(chat, key, value)
                session.commit()
                logger.info(f"Updated chat message with ID: {chat_id}")
                return chat
            logger.warning(f"Chat message with ID: {chat_id} not found")
            return None
        except Exception as e:
            session.rollback()
            logger.error(f"Error updating chat message: {e}")
            raise e
        finally:
            session.close()

    def delete_chat(self, chat_id):
        """Delete a chat message by its ID."""
        session = self.scoped_session_factory()
        try:
            chat = session.query(ParentTeacherChat).filter(ParentTeacherChat.chat_id == chat_id).one_or_none()
            if chat:
                session.delete(chat)
                session.commit()
                logger.info(f"Deleted chat message with ID: {chat_id}")
                return True
            logger.warning(f"Chat message with ID: {chat_id} not found")
            return False
        except Exception as e:
            session.rollback()
            logger.error(f"Error deleting chat message: {e}")
            raise e
        finally:
            session.close()
