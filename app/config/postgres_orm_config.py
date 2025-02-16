import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

# Load environment variables from a .env file
load_dotenv()

# Get the database URI from an environment variable, or use a default value.
DATABASE_URI = os.getenv("DATABASE_URI", "postgresql://username:password@localhost:5432/dbname")

# Create the SQLAlchemy engine.
engine = create_engine(DATABASE_URI, echo=True)

# Create a declarative base class for your ORM models.
Base = declarative_base()

# Create a session factory bound to the engine.
session_factory = sessionmaker(bind=engine)

# Create a scoped session to handle thread-local sessions.
scoped_session_factory = scoped_session(session_factory)
