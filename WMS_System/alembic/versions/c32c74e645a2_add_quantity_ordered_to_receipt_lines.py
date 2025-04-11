"""Add quantity_ordered to receipt_lines

Revision ID: c32c74e645a2
Revises: c76190fa5f4b
Create Date: 2025-04-11 16:35:19.751102

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c32c74e645a2'
down_revision: Union[str, None] = 'c76190fa5f4b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade():
    op.drop_table('receipt_lines')  # Drop old table

    op.create_table(
        'receipt_lines',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('receipt_number', sa.String(50), sa.ForeignKey('receipts.receipt_number'), nullable=False),

        sa.Column('line_number', sa.Integer),
        sa.Column('item_code', sa.String(50), nullable=False),
        sa.Column('description', sa.String(200)),
        sa.Column('upc', sa.String(50)),

        sa.Column('quantity_ordered', sa.Integer, nullable=False),
        sa.Column('quantity_expected', sa.Integer, nullable=False),
        sa.Column('quantity_received', sa.Integer, nullable=False),
        sa.Column('uom', sa.String(20)),

        sa.Column('unit_price', sa.Float),
        sa.Column('total_price', sa.Float),

        sa.Column('lot_number', sa.String(50)),
        sa.Column('expiration_date', sa.DateTime),
        sa.Column('location_received', sa.String(50)),
        sa.Column('comments', sa.String(200)),

        sa.Column('custom_1', sa.String(100)),
        sa.Column('custom_2', sa.String(100)),
        sa.Column('custom_3', sa.String(100)),
    )


def downgrade():
    op.drop_table('receipt_lines')  # In case of rollback