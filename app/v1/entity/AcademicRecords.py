from sqlalchemy import Column, Integer, String, Date, TIMESTAMP, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
import datetime
from app.config.postgres_orm_config import Base

class AcademicRecords(Base):
    __tablename__ = 'academic_records'
    __table_args__ = ({'schema': 'app'},)

    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('app.students.student_id', ondelete='CASCADE'), nullable=False)
    subject = Column(String(255), nullable=False)
    grade = Column(String(10), nullable=False)
    record_date = Column(Date, nullable=False)
    teacher_id = Column(Integer, ForeignKey('app.users.id', ondelete='SET NULL'), nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), default=datetime.datetime.now(datetime.timezone.utc))
    updated_at = Column(TIMESTAMP(timezone=True), default=datetime.datetime.now(datetime.timezone.utc), onupdate=datetime.datetime.now(datetime.timezone.utc))

    def __repr__(self):
        return f"AcademicRecords(id={self.id}, student_id={self.student_id}, subject='{self.subject}', grade='{self.grade}', record_date={self.record_date})"
