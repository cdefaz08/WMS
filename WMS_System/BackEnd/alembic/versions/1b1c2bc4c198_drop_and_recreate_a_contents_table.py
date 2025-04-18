"""Drop and recreate a_contents table

Revision ID: 1b1c2bc4c198
Revises: 53d69a2fb4d1
Create Date: 2025-04-13 14:09:20.350294

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1b1c2bc4c198'
down_revision: Union[str, None] = '53d69a2fb4d1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None



def upgrade():
    # 🚨 Drop the table first
    op.drop_table('a_contents')

    # 🧱 Recreate it with corrected column types
    op.create_table(
        'a_contents',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('location_id', sa.String, sa.ForeignKey('locations.location_id'), nullable=False),
        sa.Column('pallet_id', sa.String(50), nullable=False),
        sa.Column('item_id', sa.String(50), sa.ForeignKey('items.item_id'), nullable=False),
        sa.Column('pieces_on_hand', sa.Integer, nullable=False, default=0),
        sa.Column('receipt_info', sa.String(100), nullable=True),
        sa.Column('receipt_release_num', sa.String(50), nullable=True),
        sa.Column('date_time_last_touched', sa.DateTime, nullable=False),
        sa.Column('user_last_touched', sa.String(50), nullable=False),
    )


def downgrade():
    # Rollback: Drop the new table and recreate old version
    op.drop_table('a_contents')

    op.create_table(
        'a_contents',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('location_id', sa.String, sa.ForeignKey('locations.location_id'), nullable=False),
        sa.Column('pallet_id', sa.String(50), nullable=False),
        sa.Column('item_id', sa.String(50), sa.ForeignKey('items.item_id'), nullable=False),
        sa.Column('pieces_on_hand', sa.Integer, nullable=False, default=0),
        sa.Column('receipt_info', sa.String(100), nullable=True),
        sa.Column('receipt_release_num', sa.String(50), nullable=True),
        sa.Column('date_time_last_touched', sa.DateTime, nullable=False),
        sa.Column('user_last_touched', sa.String(50), nullable=False),
    )