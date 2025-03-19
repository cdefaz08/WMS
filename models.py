from sqlalchemy import Table, Column, Integer, String, Float, Boolean
from database import metadata

# Define the "items" table
items = Table(
    "items",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String(50)),
    Column("price", Float),
    Column("is_offer", Boolean)
)

# Define the "users" table
users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("username", String(50)),
    Column("password", String(50), nullable=False),
    Column("role", String(30))
)