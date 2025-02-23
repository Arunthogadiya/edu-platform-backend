from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
import datetime
from app.config.postgres_orm_config import Base

class Activities(Base):
    __tablename__ = 'activities'
    __table_args__ = ({'schema': 'app'},)

    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('app.students.student_id', ondelete='CASCADE'), nullable=False)
    activity_name = Column(String(255), nullable=False)
    badge = Column(String(100), nullable=True)
    description = Column(Text, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), default=datetime.datetime.now(datetime.timezone.utc))

    def __repr__(self):
        return f"Activities(id={self.id}, student_id={self.student_id}, activity_name='{self.activity_name}', badge='{self.badge}')"
