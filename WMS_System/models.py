from sqlalchemy import Table, Column, Integer, String, Float, Boolean, DateTime,Date, ForeignKey
from database import metadata , Base
from sqlalchemy.sql import func

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
    Column("vendor_id", Integer, nullable=False),
    Column("order_date", Date, nullable=False),           # <- CAMBIO A Date
    Column("expected_date", Date),                        # <- CAMBIO A Date
    Column("ship_date", Date),                            # <- CAMBIO A Date
    Column("status", String(30), default="Open"),
    Column("created_by", String(50)),
    Column("created_date", DateTime, server_default=func.now()),
    Column("modified_by", String(50)),
    Column("modified_date", DateTime, onupdate=func.now()),
    Column("ship_company_name", String(100)),
    Column("ship_address", String(150)),
    Column("ship_city", String(50)),
    Column("ship_state", String(50)),
    Column("ship_zip_code", String(20)),
    Column("ship_country", String(50)),
    Column("ship_contact_name", String(50)),
    Column("ship_contact_phone", String(30)),
    Column("ship_tax_id", String(30)),

    # Dirección de facturación (Bill To)
    Column("bill_company_name", String(100)),
    Column("bill_address", String(150)),
    Column("bill_city", String(50)),
    Column("bill_state", String(50)),
    Column("bill_zip_code", String(20)),
    Column("bill_country", String(50)),
    Column("bill_contact_name", String(50)),
    Column("bill_contact_phone", String(30)),
    Column("bill_tax_id", String(30)),

    # Custom fields
    Column("custom_1", String(100)),
    Column("custom_2", String(100)),
    Column("custom_3", String(100)),
    Column("custom_4", String(100)),
    Column("custom_5", String(100)),
    Column("comments", String(200)),
)

Order_type = Table(
    "order_type",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("order_type", String(50), nullable=False, unique=True),
    Column("description", String(50)),
    Column("document_form", String(50)),
    Column("label_form", String(50)),
)

Doc_form = Table(
    "document_form",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("document_form", String(60), nullable=False, unique=True),
    Column("description", String(50)),
    Column("action", String(50)),  # Action to be taken for this document form
    Column("template_content", String),  # Path to the template file
)

Label_form = Table(
    "label_form",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("label_form", String(60), nullable=False, unique=True),
    Column("description", String(50)),
    Column("action", String(50)),  # Action to be taken for this label form
    Column("template_content", String),  # Path to the template file
)

purchase_order_lines = Table(
    "purchase_order_lines",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("purchase_order_id", Integer, nullable=False),  # FK a purchase_orders
    Column("line_number", Integer, nullable=False),
    Column("upc", String(50), nullable=True),
    Column("item_id", Integer, nullable=False),            # FK a items
    Column("item_code",String(100)),
    Column("description", String(100)),
    Column("total_pieces", Float, nullable=False, default=0),
    Column("qty_ordered", Integer, nullable=False),
    Column("qty_expected", Integer, nullable=False),
    Column("qty_received", Integer, nullable=False),
    Column("uom", String(20), default="Pieces"),
    Column("unit_price", Float, nullable=True),
    Column("line_total", Float),
    Column("lot_number", String(50)),
    Column("expiration_date", Date),
    Column("location_received", String(50)),
    Column("comments", String(200)),
    Column("custom_1", String(100)),
    Column("custom_2", String(100)),
    Column("custom_3", String(100)),
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
    Column("created_by", String(50)),  # Foreign key ref to users
    Column("comments", String(200)),
    Column("label_form", String(50)),
    Column("document_form", String(50)),
    Column("order_type", String(50)),
    Column("carrier",String(50)),
    Column("ship_method",String(50)),
    Column("customer_PO",String(50)),
    Column("shp_to_Company",String(50)),
    Column("shp_to_Addres",String(50)),
    Column("shp_to_Addres2",String(50)),
    Column("shp_to_City",String(50)),
    Column("shp_to_State",String(50)),
    Column("shp_to_ZipCode",String(50)),
    Column("shp_to_Country",String(50)),
    Column("shp_to_ContactName",String(50)),
    Column("shp_to_ContactPhone",String(50)),
    Column("shp_to_TaxId",String(50)),
    Column("bill_to_Company",String(50)),
    Column("bill_to_Addres",String(50)),
    Column("bill_to_Addres2",String(50)),
    Column("bill_to_City",String(50)),
    Column("bill_to_State",String(50)),
    Column("bill_to_ZipCode",String(50)),
    Column("bill_to_Country",String(50)),
    Column("bill_to_ContactName",String(50)),
    Column("bill_to_ContactPhone",String(50)),
    Column("bill_to_TaxId",String(50)),
    Column("InvoiceNumber",String(50)),
    Column("Store",String(50)),
    Column("Vendor_num",String(50)),
    Column("custom_1",String(50)),
    Column("custom_2",String(50)),
    Column("custom_3",String(50)),
    Column("custom_4",String(50)),
    Column("custom_5",String(50)),

)

order_lines = Table(
    "order_lines",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("order_number", String(50), nullable=False),
    Column("item_code", String(100), nullable=False),
    Column("upc",Integer),
    Column("alt_item_id1", Integer),
    Column("alt_item_id2", Integer),
    Column("quantity", Integer, nullable=False),
    Column("unit_price", Float, nullable=False),
    Column("line_total", Float, nullable=False),
    Column("comments", String(200))
)




receipts = Table(
    "receipts",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("receipt_number", String(50), nullable=False, unique=True),
    Column("po_id", Integer, nullable=False),  # Foreign key to purchase_orders
    Column("vendor_id", Integer, nullable=False),  # Foreign key to vendors
    Column("received_by", String(50)),  # Foreign key to users
    Column("receipt_date", DateTime, nullable=False),
    Column("total_received_items", Integer),
    Column("comments", String(200)),

    # 🔽 Nuevas columnas
    Column("vendor_name", String(100)),
    Column("release_num", String(50)),
    Column("invoice_num", String(50)),
    Column("status", String(50)),
    Column("date_shipped", DateTime),
    Column("date_expected", DateTime),
    Column("date_received", DateTime),
    Column("label_form", String(50)),
    Column("document_form", String(50)),
    Column("close_receipt", Boolean, default=False),
    Column("carrier", String(100)),
    Column("seal_num", String(50)),
    Column("created_by", String(50)),
    Column("created_date", DateTime),

    # Ship From
    Column("ship_from_company", String(100)),
    Column("ship_from_address", String(150)),
    Column("ship_from_address2", String(150)),
    Column("ship_from_city", String(50)),
    Column("ship_from_state", String(50)),
    Column("ship_from_zip", String(20)),
    Column("ship_from_country", String(50)),
    Column("ship_from_contact_name", String(100)),
    Column("ship_from_contact_phone", String(30)),
    Column("ship_from_tax_id", String(30)),

    # Bill To
    Column("bill_to_company", String(100)),
    Column("bill_to_address", String(150)),
    Column("bill_to_address2", String(150)),
    Column("bill_to_city", String(50)),
    Column("bill_to_state", String(50)),
    Column("bill_to_zip", String(20)),
    Column("bill_to_country", String(50)),
    Column("bill_to_contact_name", String(100)),
    Column("bill_to_contact_phone", String(30)),
    Column("bill_to_tax_id", String(30)),

    # Custom fields
    Column("custom_1", String(100)),
    Column("custom_2", String(100)),
    Column("custom_3", String(100)),
    Column("custom_4", String(100)),
    Column("custom_5", String(100)),
    Column("custom_6", String(100)),
    Column("custom_7", String(100)),
    Column("custom_8", String(100)),
    Column("custom_9", String(100)),
    Column("custom_10", String(100)),
)

receipt_lines = Table(
    "receipt_lines",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),

    # 👇 Foreign key using receipt_number instead of receipt_id
    Column("receipt_number", String(50), ForeignKey("receipts.receipt_number"), nullable=False),

    Column("line_number", Integer),
    Column("item_id", String(50), ForeignKey("items.id"), nullable=False),
    Column("item_code", String(50), nullable=False),
    Column("description", String(200)),
    Column("upc", String(50)),
    Column("quantity_ordered", Integer, nullable=False),
    Column("quantity_expected", Integer, nullable=False),
    Column("quantity_received", Integer, nullable=False),
    Column("uom", String(20)),
    Column("unit_price", Float),
    Column("total_price", Float),
    Column("lot_number", String(50)),
    Column("expiration_date", DateTime),
    Column("location_received", String(50)),
    Column("comments", String(200)),

    Column("custom_1", String(100)),
    Column("custom_2", String(100)),
    Column("custom_3", String(100)),
)


item_maintance = Table(
    "item_maintance",
    metadata,

    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("item_id", String(50), ForeignKey("items.item_id"), nullable=False),

    # Flags
    Column("is_default", Boolean, default=False),  # Solo una configuración por ítem puede ser predeterminada

    # Dimensiones
    Column("pallet_length", Float),
    Column("pallet_width", Float),
    Column("pallet_height", Float),

    Column("case_length", Float),
    Column("case_width", Float),
    Column("case_height", Float),

    Column("piece_length", Float),
    Column("piece_width", Float),
    Column("piece_height", Float),

    Column("inner_length", Float),
    Column("inner_width", Float),
    Column("inner_height", Float),

    # Pesos
    Column("pallet_weight", Float),
    Column("case_weight", Float),
    Column("piece_weight", Float),
    Column("inner_weight", Float),

    # Cantidades por unidad
    Column("boxes_per_pallet", Integer),
    Column("pieces_per_case", Integer),
    Column("inners_per_piece", Integer),

    # UOM y códigos de barra
    Column("unit_of_measure", String(20)),  # EA, BOX, INNER, etc.
    Column("barcode_case", String(50)),
    Column("barcode_pallet", String(50)),
    Column("barcode_inner", String(50)),

    # Información adicional
    Column("configuration_name", String(100)),  # Ejemplo: Retail Config, Bulk Config
    Column("notes", String(200)),
)

a_contents = Table(
    "a_contents",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("location_id", String, ForeignKey("locations.location_id"), nullable=False),
    Column("pallet_id", String(50), nullable=True),
    Column("item_id", String(50), ForeignKey("items.item_id"), nullable=True),
    Column("pieces_on_hand", Integer, nullable=False, default=0),
    Column("receipt_info", String(100), nullable=True),
    Column("receipt_release_num", String(50), nullable=True),
    Column("date_time_last_touched", DateTime, nullable=False),
    Column("user_last_touched", String(50), nullable=False),
)