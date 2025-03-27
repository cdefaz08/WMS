from sqlalchemy import Table, Column, Integer, String, Float, Boolean
from database import metadata

# Define the "items" table
items = Table(
    "items",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("item_id", String(50), nullable=False),
    Column("description", String(60),nullable=False),
    Column("color", String),
    Column("size",String),
    Column("price", Float),
    Column("upc", Integer ,nullable=False),
    Column("alt_item_id1", Integer),
    Column("alt_item_id2", Integer),
    Column("item_class", String(50), nullable =True ,default="STND"),
    Column("description2", String(50)),
    Column("is_offer", Boolean),
    Column("default_cfg", String(10)),
    Column("brand",String(30)),
    Column("style",String(30)),
    Column("custum1",String(30)),
    Column("custum2",String(30)),
    Column("custum3",String(30)),
    Column("custum4",String(30)),
    Column("custum5",String(30)),
    Column("custum6",String(30)),
)

# Define the "users" table
users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("username", String(50), nullable=False),
    Column("password", String(50), nullable=False),
    Column("full_name",String(30)),
    Column("max_logins",Integer,nullable=False ,default="0"),
    Column("email_addr",String),
    Column("pall_cap",Integer, nullable=False, default="0"),
    Column("comments",String),
    Column("role", String(30), nullable=False)
)


item_class = Table(
    "item_class",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("item_class_id", String, nullable=False),
    Column("description", String(20))
)