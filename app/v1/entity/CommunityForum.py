from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
import datetime
from app.config.postgres_orm_config import Base

class CommunityForum(Base):
    __tablename__ = 'community_forum'
    __table_args__ = ({'schema': 'app'},)

    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey('app.users.id', ondelete='CASCADE'), nullable=False)
    student_id = Column(Integer, ForeignKey('app.students.student_id', ondelete='CASCADE'), nullable=False)
    title = Column(String(255), nullable=True)
    content = Column(Text, nullable=False)
    language = Column(String(50), nullable=False)
    is_anonymous = Column(Boolean, default=False)
    is_reply = Column(Boolean, default=False)
    forum_id = Column(Integer, ForeignKey('app.community_forum.id', ondelete='CASCADE'), nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), default=datetime.datetime.now(datetime.timezone.utc))
    updated_at = Column(TIMESTAMP(timezone=True), default=datetime.datetime.now(datetime.timezone.utc), onupdate=datetime.datetime.now(datetime.timezone.utc))

    def __repr__(self):
        return f"CommunityForum(id={self.id}, parent_id={self.parent_id}, student_id={self.student_id}, title='{self.title}', content='{self.content}', language='{self.language}', is_anonymous={self.is_anonymous}, is_reply={self.is_reply}, forum_id={self.forum_id})"
