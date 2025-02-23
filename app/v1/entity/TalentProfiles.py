from sqlalchemy import Column, Integer, String, JSON, TIMESTAMP, ForeignKey, Numeric
from sqlalchemy.ext.declarative import declarative_base
import datetime
from app.config.postgres_orm_config import Base

class TalentProfiles(Base):
    __tablename__ = 'talent_profiles'
    __table_args__ = ({'schema': 'app'},)

    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('app.students.student_id', ondelete='CASCADE'), nullable=False)
    domain = Column(String(255), nullable=False)
    performance_data = Column(JSON, nullable=False)
    score = Column(Numeric(10, 2), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), default=datetime.datetime.now(datetime.timezone.utc))
    updated_at = Column(TIMESTAMP(timezone=True), default=datetime.datetime.now(datetime.timezone.utc), onupdate=datetime.datetime.now(datetime.timezone.utc))

    def __repr__(self):
        return f"TalentProfiles(id={self.id}, student_id={self.student_id}, domain='{self.domain}', score={self.score})"
