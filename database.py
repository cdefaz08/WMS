from databases import Database
from sqlalchemy import create_engine, MetaData

Database_URL = "sqlite:///./test.db"

database = Database(Database_URL)

engine = create_engine(Database_URL)
metadata = MetaData()