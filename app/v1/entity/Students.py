from sqlalchemy import Column, Integer, String, Date, TIMESTAMP, CheckConstraint
from sqlalchemy.ext.declarative import declarative_base
import datetime
from app.config.postgres_orm_config import Base

class Students(Base):
    __tablename__ = 'students'
    __table_args__ = ({'schema': 'app'},)

    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, primary_key=True)
    student_name = Column(String(255), nullable=False)
    parent_name = Column(String(255), nullable=False)
    parent_phone = Column(String(20))
    class_value = Column(String(50), nullable=False)
    section = Column(String(20))
    date_of_birth = Column(Date)
    gender = Column(String(10))
    created_at = Column(TIMESTAMP(timezone=True), default=datetime.datetime.now(datetime.timezone.utc))
    updated_at = Column(TIMESTAMP(timezone=True), default=datetime.datetime.now(datetime.timezone.utc), onupdate=datetime.datetime.now(datetime.timezone.utc))

    def __repr__(self):
        return f"Students(student_id={self.student_id}, student_name='{self.student_name}', parent_name='{self.parent_name}')"
