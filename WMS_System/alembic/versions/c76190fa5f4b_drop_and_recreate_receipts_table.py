"""Drop and recreate receipts table

Revision ID: c76190fa5f4b
Revises: 2eb35b974ee4
Create Date: 2025-04-11 16:26:50.385019

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c76190fa5f4b'
down_revision: Union[str, None] = '2eb35b974ee4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # ⚠️ Drop the existing table (be careful - this will delete data)
    op.drop_table('receipts')

    # ✅ Recreate the table with updated columns
    op.create_table(
        'receipts',
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("receipt_number", sa.String(50), nullable=False, unique=True),
        sa.Column("po_id", sa.Integer, nullable=False),
        sa.Column("vendor_id", sa.Integer, nullable=False),
        sa.Column("received_by", sa.String(50)),
        sa.Column("receipt_date", sa.DateTime, nullable=False),
        sa.Column("total_received_items", sa.Integer),
        sa.Column("comments", sa.String(200)),

        # New fields
        sa.Column("vendor_name", sa.String(100)),
        sa.Column("release_num", sa.String(50)),
        sa.Column("invoice_num", sa.String(50)),
        sa.Column("status", sa.String(50)),
        sa.Column("date_shipped", sa.DateTime),
        sa.Column("date_expected", sa.DateTime),
        sa.Column("date_received", sa.DateTime),
        sa.Column("label_form", sa.String(50)),
        sa.Column("document_form", sa.String(50)),
        sa.Column("close_receipt", sa.Boolean, default=False),
        sa.Column("carrier", sa.String(100)),
        sa.Column("seal_num", sa.String(50)),
        sa.Column("created_by", sa.String(50)),
        sa.Column("created_date", sa.DateTime),

        # Ship From
        sa.Column("ship_from_company", sa.String(100)),
        sa.Column("ship_from_address", sa.String(150)),
        sa.Column("ship_from_address2", sa.String(150)),
        sa.Column("ship_from_city", sa.String(50)),
        sa.Column("ship_from_state", sa.String(50)),
        sa.Column("ship_from_zip", sa.String(20)),
        sa.Column("ship_from_country", sa.String(50)),
        sa.Column("ship_from_contact_name", sa.String(100)),
        sa.Column("ship_from_contact_phone", sa.String(30)),
        sa.Column("ship_from_tax_id", sa.String(30)),

        # Bill To
        sa.Column("bill_to_company", sa.String(100)),
        sa.Column("bill_to_address", sa.String(150)),
        sa.Column("bill_to_address2", sa.String(150)),
        sa.Column("bill_to_city", sa.String(50)),
        sa.Column("bill_to_state", sa.String(50)),
        sa.Column("bill_to_zip", sa.String(20)),
        sa.Column("bill_to_country", sa.String(50)),
        sa.Column("bill_to_contact_name", sa.String(100)),
        sa.Column("bill_to_contact_phone", sa.String(30)),
        sa.Column("bill_to_tax_id", sa.String(30)),

        # Custom
        sa.Column("custom_1", sa.String(100)),
        sa.Column("custom_2", sa.String(100)),
        sa.Column("custom_3", sa.String(100)),
        sa.Column("custom_4", sa.String(100)),
        sa.Column("custom_5", sa.String(100)),
        sa.Column("custom_6", sa.String(100)),
        sa.Column("custom_7", sa.String(100)),
        sa.Column("custom_8", sa.String(100)),
        sa.Column("custom_9", sa.String(100)),
        sa.Column("custom_10", sa.String(100)),
    )


def downgrade():
    op.drop_table('receipts')