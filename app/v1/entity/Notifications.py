from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, ForeignKey, Enum
from sqlalchemy.ext.declarative import declarative_base
import datetime
from app.config.postgres_orm_config import Base
from sqlalchemy.dialects.postgresql import ENUM

notification_status_enum = ENUM('pending', 'delivered', 'failed', name='notification_status', create_type=False)

class Notifications(Base):
    __tablename__ = 'notifications'
    __table_args__ = ({'schema': 'app'},)

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('app.users.id', ondelete='CASCADE'), nullable=False)
    message = Column(Text, nullable=False)
    language = Column(String(10), nullable=False)
    urgency = Column(Integer, nullable=False)
    delivery_method = Column(String(50), nullable=False)
    status = Column(notification_status_enum, nullable=False, default='pending')
    created_at = Column(TIMESTAMP(timezone=True), default=datetime.datetime.now(datetime.timezone.utc))

    def __repr__(self):
        return f"Notifications(id={self.id}, user_id={self.user_id}, message='{self.message}', status='{self.status}')"
