from sqlalchemy import Table, Column, Integer, String, Float, Boolean, DateTime,Time
from database import metadata , Base

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
    



restock_classes = Table(
    "restock_classes",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("class_name", String(15), nullable=False, unique=True),
    Column("description", String(50)),
)



putaway_classes = Table(
    "putaway_classes",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("class_name", String(15), nullable=False, unique=True),
    Column("description", String(50)),
)


pick_classes = Table(
    "pick_classes",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("class_name", String(15), nullable=False, unique=True),
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

vendors = Table(
    "vendors",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("vendor_code", String(50), nullable=False, unique=True),
    Column("vendor_name", String(100), nullable=False),
    Column("contact_name", String(50)),
    Column("tax_id", String(30)),
    Column("phone", String(30)),
    Column("email", String(50)),
    Column("address", String(150)),
    Column("city", String(50)),
    Column("state", String(30)),
    Column("zip_code", String(20)),
    Column("country", String(30)),
    Column("notes", String(200)),
)


purchase_orders = Table(
    "purchase_orders",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("po_number", String(50), nullable=False, unique=True),
    Column("vendor_id", Integer, nullable=False),  # Foreign key ref to vendors
    Column("order_date", DateTime, nullable=False),
    Column("expected_date", DateTime),
    Column("status", String(30), default="Open"),  # Open, Received, Cancelled, etc.
    Column("created_by", Integer),  # Foreign key ref to users
    Column("comments", String(200)),
)

purchase_order_lines = Table(
    "purchase_order_lines",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("purchase_order_id", Integer, nullable=False),  # FK to purchase_orders
    Column("item_id", Integer, nullable=False),            # FK to items
    Column("quantity", Integer, nullable=False),
    Column("unit_price", Float, nullable=True),
    Column("line_total", Float),  # quantity * unit_price
    Column("comments", String(200))
)


orders = Table(
    "orders",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("order_number", String(50), nullable=False, unique=True),
    Column("customer_name", String(100), nullable=False),
    Column("order_date", DateTime, nullable=False),
    Column("ship_date", DateTime),
    Column("status", String(30), default="Pending"),  # Pending, Shipped, Cancelled
    Column("total_amount", Float),
    Column("created_by", Integer),  # Foreign key ref to users
    Column("comments", String(200)),
)

order_lines = Table(
    "order_lines",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("order_id", Integer, nullable=False),     # FK to orders
    Column("item_id", Integer, nullable=False),      # FK to items
    Column("quantity", Integer, nullable=False),
    Column("unit_price", Float),
    Column("line_total", Float),  # Optional: calculated as quantity * unit_price
    Column("comments", String(200)),
)



receipts = Table(
    "receipts",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("receipt_number", String(50), nullable=False, unique=True),
    Column("po_id", Integer, nullable=False),  # Foreign key to purchase_orders
    Column("vendor_id", Integer, nullable=False),  # Foreign key to vendors
    Column("received_by", Integer),  # Foreign key to users
    Column("receipt_date", DateTime, nullable=False),
    Column("total_received_items", Integer),
    Column("comments", String(200)),
)
