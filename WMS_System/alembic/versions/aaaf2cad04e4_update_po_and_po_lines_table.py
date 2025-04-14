"""Update PO and PO_lines table

Revision ID: aaaf2cad04e4
Revises: e5bf0cdcf855
Create Date: 2025-04-14 12:15:20.966585

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'aaaf2cad04e4'
down_revision: Union[str, None] = 'e5bf0cdcf855'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Drop old tables
    op.drop_table('purchase_order_lines')
    op.drop_table('purchase_orders')

    # Recreate purchase_orders table
    op.create_table(
        'purchase_orders',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('po_number', sa.String(50), nullable=False, unique=True),
        sa.Column('vendor_id', sa.Integer(), nullable=False),
        sa.Column('order_date', sa.DateTime(), nullable=False),
        sa.Column('expected_date', sa.DateTime()),
        sa.Column('ship_date', sa.DateTime()),
        sa.Column('status', sa.String(30), default='Open'),
        sa.Column('created_by', sa.Integer()),
        sa.Column('created_date', sa.DateTime(), server_default=sa.func.now()),
        sa.Column('modified_by', sa.String(50)),
        sa.Column('modified_date', sa.DateTime(), onupdate=sa.func.now()),
        sa.Column('comments', sa.String(200)),
    )

    # Recreate purchase_order_lines table
    op.create_table(
        'purchase_order_lines',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('purchase_order_id', sa.Integer(), nullable=False),
        sa.Column('item_id', sa.Integer(), nullable=False),
        sa.Column('qty_ordered', sa.Integer(), nullable=False),
        sa.Column('qty_received', sa.Integer(), nullable=False),
        sa.Column('unit_price', sa.Float(), nullable=True),
        sa.Column('line_total', sa.Float()),
        sa.Column('comments', sa.String(200)),
    )


def downgrade():
    # Drop both tables
    op.drop_table('purchase_order_lines')
    op.drop_table('purchase_orders')
