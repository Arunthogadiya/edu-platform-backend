from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
import datetime
from app.config.postgres_orm_config import Base

class CommunityPoll(Base):
    __tablename__ = 'community_poll'
    __table_args__ = ({'schema': 'app'},)

    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey('app.users.id', ondelete='CASCADE'), nullable=False)
    student_id = Column(Integer, ForeignKey('app.students.student_id', ondelete='CASCADE'), nullable=False)
    question = Column(Text, nullable=True)
    options = Column(Text, nullable=True)  # JSON string of options
    votes = Column(Text, nullable=False)  # JSON string of votes
    created_at = Column(TIMESTAMP(timezone=True), default=datetime.datetime.now(datetime.timezone.utc))
    updated_at = Column(TIMESTAMP(timezone=True), default=datetime.datetime.now(datetime.timezone.utc), onupdate=datetime.datetime.now(datetime.timezone.utc))

    def __repr__(self):
        return f"CommunityPoll(id={self.id}, parent_id={self.parent_id}, student_id={self.student_id}, question='{self.question}', options='{self.options}', votes='{self.votes}')"
