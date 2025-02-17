from sqlalchemy import Column, Integer, String, Date, TIMESTAMP, Text, ForeignKey, Enum
from sqlalchemy.ext.declarative import declarative_base
import datetime
from app.config.postgres_orm_config import Base
from sqlalchemy.dialects.postgresql import ENUM

behavior_source_enum = ENUM('school', 'home', name='behavior_source', create_type=False)

class BehaviorRecords(Base):
    __tablename__ = 'behavior_records'
    __table_args__ = ({'schema': 'app'},)

    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('app.students.student_id', ondelete='CASCADE'), nullable=False)
    logged_by = Column(Integer, ForeignKey('app.users.id', ondelete='SET NULL'), nullable=True)
    source = Column(behavior_source_enum, nullable=False)
    behaviour_type = Column(String(255), nullable=True)
    sentiment_score = Column(Integer, nullable=True)
    comment = Column(Text, nullable=True)
    record_date = Column(Date, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), default=datetime.datetime.now(datetime.timezone.utc))

    def __repr__(self):
        return f"BehaviorRecords(id={self.id}, student_id={self.student_id}, source='{self.source}', behaviour_type='{self.behaviour_type}', record_date={self.record_date})"
