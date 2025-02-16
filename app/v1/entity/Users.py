from sqlalchemy import Column, Integer, String, Enum, TIMESTAMP, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import ENUM
import datetime
from app.config.postgres_orm_config import Base
from app.v1.entity.Students import Students

class Users(Base):
    __tablename__ = 'users'
    __table_args__ = ({'schema': 'app'},)

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(ENUM('parent', 'teacher', 'admin', name='user_role'), nullable=False, default='parent')
    language = Column(String(10), nullable=False, default='en')
    phone = Column(String(20))
    student_id = Column(Integer, ForeignKey('app.students.student_id'), nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), default=datetime.datetime.now(datetime.timezone.utc))
    updated_at = Column(TIMESTAMP(timezone=True), default=datetime.datetime.now(datetime.timezone.utc), onupdate=datetime.datetime.now(datetime.timezone.utc))

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        if self.role != 'parent':
            self.student_id = None

    def __repr__(self):
        return f"Users(id={self.id}, name='{self.name}', email='{self.email}', role='{self.role}')"

    def __eq__(self, other):
        if isinstance(other, Users):
            return self.id == other.id and self.email == other.email
        return False

    def __hash__(self):
        return hash((self.id, self.email))


print(Base.metadata.tables.keys())