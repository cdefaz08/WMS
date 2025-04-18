"""Updated Orders Table modify created_by column from INTEGER to STRING"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column
from sqlalchemy import String, Integer

# revision identifiers, used by Alembic.
revision = 'ae8b445b3302'
down_revision = 'fe6a01060dec'
branch_labels = None
depends_on = None

def upgrade():
    # 1. Create new table
    op.execute("""
        CREATE TABLE orders_new4 (
            id INTEGER PRIMARY KEY,
            order_number TEXT NOT NULL,
            customer_name TEXT NOT NULL,
            order_date TEXT,
            ship_date TEXT,
            status TEXT,
            total_amount REAL,
            created_by TEXT,
            comments TEXT,
            label_form TEXT,
            document_form TEXT,
            order_type TEXT,
            carrier TEXT,
            ship_method TEXT,
            "Store" TEXT,
            "InvoiceNumber" TEXT,
            "Vendor_num" TEXT,
            shp_to_City TEXT,
            shp_to_State TEXT,
            shp_to_ZipCode TEXT,
            shp_to_Country TEXT,
            shp_to_ContactName TEXT,
            shp_to_ContactPhone TEXT,
            shp_to_TaxId TEXT,
            shp_to_Company TEXT,
            shp_to_Addres TEXT,
            bill_to_City TEXT,
            bill_to_State TEXT,
            bill_to_ZipCode TEXT,
            bill_to_Country TEXT,
            bill_to_ContactName TEXT,
            bill_to_ContactPhone TEXT,
            bill_to_TaxId TEXT,
            bill_to_Company TEXT,
            bill_to_Address TEXT,
            custom_1 TEXT,
            custom_2 TEXT,
            custom_3 TEXT,
            custom_4 TEXT,
            custom_5 TEXT
        );
    """)

    # 2. Copy data (cast created_by to TEXT)
    op.execute("""
        INSERT INTO orders_new SELECT 
            id, order_number, customer_name, order_date, ship_date, status, total_amount,
            CAST(created_by AS TEXT), comments, label_form, document_form, order_type,
            carrier, ship_method, "Store", "InvoiceNumber", "Vendor_num",
            shp_to_City, shp_to_State, shp_to_ZipCode, shp_to_Country,
            shp_to_ContactName, shp_to_ContactPhone, shp_to_TaxId, shp_to_Company, shp_to_Addres,
            bill_to_City, bill_to_State, bill_to_ZipCode, bill_to_Country,
            bill_to_ContactName, bill_to_ContactPhone, bill_to_TaxId, bill_to_Company, bill_to_Addres,
            custom_1, custom_2, custom_3, custom_4, custom_5
        FROM orders;
    """)

    # 3. Drop old table
    op.execute("DROP TABLE orders;")

    # 4. Rename new table
    op.execute("ALTER TABLE orders_new4 RENAME TO orders;")


def downgrade():
    # reverse: convert created_by from TEXT back to INTEGER
    op.execute("""
        CREATE TABLE orders_old (
            id INTEGER PRIMARY KEY,
            order_number TEXT NOT NULL,
            customer_name TEXT NOT NULL,
            order_date TEXT,
            ship_date TEXT,
            status TEXT,
            total_amount REAL,
            created_by INTEGER,
            comments TEXT,
            label_form TEXT,
            document_form TEXT,
            order_type TEXT,
            carrier TEXT,
            ship_method TEXT,
            "Store" TEXT,
            "InvoiceNumber" TEXT,
            "Vendor_num" TEXT,
            shp_to_City TEXT,
            shp_to_State TEXT,
            shp_to_ZipCode TEXT,
            shp_to_Country TEXT,
            shp_to_ContactName TEXT,
            shp_to_ContactPhone TEXT,
            shp_to_TaxId TEXT,
            shp_to_Company TEXT,
            shp_to_Addres TEXT,
            bill_to_City TEXT,
            bill_to_State TEXT,
            bill_to_ZipCode TEXT,
            bill_to_Country TEXT,
            bill_to_ContactName TEXT,
            bill_to_ContactPhone TEXT,
            bill_to_TaxId TEXT,
            bill_to_Company TEXT,
            bill_to_Addres TEXT,
            custom_1 TEXT,
            custom_2 TEXT,
            custom_3 TEXT,
            custom_4 TEXT,
            custom_5 TEXT
        );
    """)

    op.execute("""
        INSERT INTO orders_old SELECT 
            id, order_number, customer_name, order_date, ship_date, status, total_amount,
            CAST(created_by AS INTEGER), comments, label_form, document_form, order_type,
            carrier, ship_method, "Store", "InvoiceNumber", "Vendor_num",
            shp_to_City, shp_to_State, shp_to_ZipCode, shp_to_Country,
            shp_to_ContactName, shp_to_ContactPhone, shp_to_TaxId, shp_to_Company, shp_to_Addres,
            bill_to_City, bill_to_State, bill_to_ZipCode, bill_to_Country,
            bill_to_ContactName, bill_to_ContactPhone, bill_to_TaxId, bill_to_Company, bill_to_Addres,
            custom_1, custom_2, custom_3, custom_4, custom_5
        FROM orders;
    """)

    op.execute("DROP TABLE orders;")
    op.execute("ALTER TABLE orders_old RENAME TO orders;")
