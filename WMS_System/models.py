from sqlalchemy import Table, Column, Integer, String, Float, Boolean, DateTime,Time
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

locations = Table(
    "locations",
    metadata,
    Column("location_id",String,primary_key=True),
    Column("location_type",String, nullable=False, default="STND"),
    Column("scan_location",String),
    Column("black_hole_flag",String(1),default="N"),
    Column("proximiti_in",String),
    Column("proximiti_out",String),
    Column("has_assign_flag",String(1),default="N"),
    Column("has_contents_flag",String(1),default="N"),
    Column("has_pending_flag",String(1),default="N"),
    Column("putaway_class",String),
    Column("pick_class",String),
    Column("rstk_class",String),
    Column("blocked_code",String),
    Column("palle_cap",Integer, default=0),
    Column("carton_cap",Integer, default=0),
    Column("max_weight",Float, default=0.0),
    Column("max_height",Float, default=0.0),
    Column("max_width",Float, default=0.0),
    Column("max_depth",Float, default=0.0),
    Column("uom_max_weight",String),
    Column("uom_max_height",String),
    Column("uom_max_width",String),
    Column("uom_max_depth",String),
    Column("uom_carton_cap",String),
    Column("pallet_qty_act",Integer, default=0),
    Column("carton_qty_act",Integer, default=0),
    Column("aisle",String),
    Column("bay",String),
    Column("loc_level",String),
    Column("slot",String),
    Column("pnd_location_id1",String),
    Column("pnd_location_id2",String),
    Column("last_touch",DateTime),
)
    
restock_clases = Table(
    "restock_clases",
    metadata,
    Column("id",Integer, primary_key=True, autoincrement=True),
    Column("class_name", String(15)),
    Column("description", String(50)),
)

putaway_clases = Table(
    "putaway_clases",
    metadata,
    Column("id",Integer, primary_key=True, autoincrement=True),
    Column("class_name", String(15)),
    Column("description", String(50)),
)

pick_clases = Table(
    "pick_clases",
    metadata,
    Column("id",Integer, primary_key=True, autoincrement=True),
    Column("class_name", String(15)),
    Column("description", String(50)),
)

block_codes = Table(
    "block_codes",
    metadata,
    Column("id",Integer, primary_key=True, autoincrement=True),
    Column("code",String(20),nullable=False),
    Column("description",String(50),nullable=False),
)

cycle_codes = Table(
    "cycle_codes",
    metadata,
    Column("id",Integer, primary_key=True, autoincrement=True),
    Column("code",String(20),nullable=False),
    Column("description",String(50),nullable=False),
)

proximities = Table(
    "proximities",
    metadata,
    Column("id",Integer, primary_key=True, autoincrement=True),
    Column("proximity",String(10), nullable=False),
    Column("movers",Integer,default=0)
)



location_types = Table(
    "location_type",
    metadata,
    Column("location_type",String,primary_key=True),
    Column("description",String),
    Column("system_flag",String(1),default="N"),
    Column("sto_pall_flag",String(1),default="N"),
    Column("sto_pall_cart_flag",String(1),default="N"),
    Column("sto_pall_con_flag",String(1),default="N"),
    Column("sto_cart_flag",String(1),default="N"),
    Column("sto_cont_flag",String(1),default="N"),
    Column("mix_item_flag",String(1),default="N"),
    Column("mix_cfg_flag",String(1),default="N"),
    Column("mix_trackingdate_flag",String(1),default="N"),
    Column("mix_receivingdate_flag",String(1),default="N"),
    Column("mix_recdate_flag",String(1),default="N"),
    Column("merge_flag",String(1),default="N"),
    Column("trash_pall",String(1),default="N"),
    Column("merge_cfg_code",String(1),default="N"),
    Column("merge_trackingdate",String(1),default="N"),
    Column("merge_inventory_type",String(1),default="N"),
    Column("merge_receiving_date",String(1),default="N"),
    Column("pick_pallet_flag",String(1),default="N"),
    Column("pick_cart_flag",String(1),default="N"),
    Column("pick_piece_flag",String(1),default="N"),

)