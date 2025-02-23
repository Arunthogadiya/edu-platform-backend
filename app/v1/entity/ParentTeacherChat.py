from sqlalchemy import Column, Integer, Text, TIMESTAMP, ForeignKey, Enum, Boolean
from sqlalchemy.ext.declarative import declarative_base
import datetime
from app.config.postgres_orm_config import Base
from sqlalchemy.dialects.postgresql import ENUM

sender_type_enum = ENUM('teacher', 'parent', name='sender_type', create_type=False)

class ParentTeacherChat(Base):
    __tablename__ = 'parent_teacher_chat'
    __table_args__ = ({'schema': 'app'},)

    chat_id = Column(Integer, primary_key=True)
    teacher_id = Column(Integer, ForeignKey('app.users.id', ondelete='CASCADE'), nullable=False)
    parent_id = Column(Integer, ForeignKey('app.users.id', ondelete='CASCADE'), nullable=False)
    sender = Column(sender_type_enum, nullable=False)
    message = Column(Text, nullable=False)
    is_read = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP(timezone=True), default=datetime.datetime.now(datetime.timezone.utc))

    def __repr__(self):
        return f"ParentTeacherChat(chat_id={self.chat_id}, teacher_id={self.teacher_id}, parent_id={self.parent_id}, sender='{self.sender}', message='{self.message}')"
