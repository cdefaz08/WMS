from databases import Database
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLite DB path
DATABASE_URL = "sqlite:///./test.db"

# Async support (if needed)
database = Database(DATABASE_URL)

# SQLAlchemy engine & session (sync)
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

# For table metadata
Base = declarative_base()
metadata = MetaData()
