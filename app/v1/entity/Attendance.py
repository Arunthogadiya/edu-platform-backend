from sqlalchemy import Column, Integer, Date, TIMESTAMP, Text, Enum, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
import datetime
from app.config.postgres_orm_config import Base
from sqlalchemy.dialects.postgresql import ENUM

attendance_status_enum = ENUM('present', 'absence', name='attendance_status', create_type=False)

class Attendance(Base):
    __tablename__ = 'attendance'
    __table_args__ = ({'schema': 'app'},)

    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('app.students.student_id', ondelete='CASCADE'), nullable=False)
    attendance_date = Column(Date, nullable=False)
    status = Column(attendance_status_enum, nullable=False, default='present')
    notes = Column(Text, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), default=datetime.datetime.now(datetime.timezone.utc))

    def __repr__(self):
        return f"Attendance(id={self.id}, student_id={self.student_id}, attendance_date={self.attendance_date}, status='{self.status}')"
