from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, TIMESTAMP, LargeBinary
from app.config.postgres_orm_config import Base
import datetime

class AudioResource(Base):
    __tablename__ = 'audio_resources'
    __table_args__ = ({'schema': 'app'},)
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    audio_data = Column(LargeBinary, nullable=False)
    teacher_id = Column(Integer, ForeignKey('app.users.id', ondelete='CASCADE'), nullable=False)
    class_value = Column(String(50), nullable=False)
    section = Column(String(20), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), default=datetime.datetime.now(datetime.timezone.utc))
    updated_at = Column(TIMESTAMP(timezone=True), default=datetime.datetime.now(datetime.timezone.utc), onupdate=datetime.datetime.now(datetime.timezone.utc))
