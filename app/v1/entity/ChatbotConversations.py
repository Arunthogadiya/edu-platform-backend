from sqlalchemy import Column, Integer, Text, TIMESTAMP, ForeignKey, JSON, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
import datetime
from app.config.postgres_orm_config import Base

class ChatbotConversations(Base):
    __tablename__ = 'chatbot_conversations'
    __table_args__ = ({'schema': 'app'},)

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('app.users.id', ondelete='CASCADE'), nullable=False)
    chat_id = Column(UUID(as_uuid=True), nullable=False)
    conversation_id = Column(UUID(as_uuid=True), nullable=False)
    query = Column(Text, nullable=False)
    response = Column(JSON, nullable=False)
    emotion = Column(String, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), default=datetime.datetime.now(datetime.timezone.utc))

    def __repr__(self):
        return f"ChatbotConversations(id={self.id}, user_id={self.user_id}, chat_id={self.chat_id}, conversation_id={self.conversation_id})"
