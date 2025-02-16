import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from urllib.parse import quote
from sqlalchemy import MetaData

# Load environment variables from a .env file
load_dotenv()

# Ensure the .env file is loaded correctly
if not os.environ.get("DB_USERNAME"):
    raise EnvironmentError("Failed to load .env file or DB_USERNAME not set")

# Get the database URI components from environment variables
username = os.environ.get("DB_USERNAME")
password = quote(os.environ.get("DB_PASSWORD"))
host = os.environ.get("DB_HOST")
port = os.environ.get("DB_PORT")
database = os.environ.get("DB_NAME")

# Construct the database URI
DATABASE_URI = f"postgresql://{username}:{password}@{host}:{port}/{database}"

# Create the SQLAlchemy engine.
engine = create_engine(DATABASE_URI, echo=True)

# Create a declarative base class for your ORM models.
Base = declarative_base()

# Create a session factory bound to the engine.
session_factory = sessionmaker(bind=engine)

# Create a scoped session to handle thread-local sessions.
scoped_session_factory = scoped_session(session_factory)

# Optionally, specify the default schema here if you want all tables to use it
metadata = MetaData(schema="app")