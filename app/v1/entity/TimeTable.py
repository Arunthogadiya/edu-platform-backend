from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
import datetime
from app.config.postgres_orm_config import Base

class TimeTable(Base):
    __tablename__ = 'time_table'
    __table_args__ = ({'schema': 'app'},)

    id = Column(Integer, primary_key=True)
    class_value = Column(String(50), nullable=False)
    section = Column(String(20), nullable=False)
    subject = Column(String(255), nullable=False)
    teacher_id = Column(Integer, ForeignKey('app.users.id', ondelete='SET NULL'), nullable=True)
    day_of_week = Column(String(20), nullable=False)
    start_time = Column(TIMESTAMP(timezone=True), nullable=False)
    end_time = Column(TIMESTAMP(timezone=True), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), default=datetime.datetime.now(datetime.timezone.utc))
    updated_at = Column(TIMESTAMP(timezone=True), default=datetime.datetime.now(datetime.timezone.utc), onupdate=datetime.datetime.now(datetime.timezone.utc))

    def __repr__(self):
        return f"TimeTable(id={self.id}, class_value='{self.class_value}', section='{self.section}', subject='{self.subject}', day_of_week='{self.day_of_week}', start_time={self.start_time}, end_time={self.end_time})"
