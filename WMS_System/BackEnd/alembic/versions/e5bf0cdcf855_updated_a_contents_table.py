"""UPdated a_contents Table

Revision ID: e5bf0cdcf855
Revises: 1b1c2bc4c198
Create Date: 2025-04-13 14:44:20.856324

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e5bf0cdcf855'
down_revision: Union[str, None] = '1b1c2bc4c198'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade():
    # Drop the existing table
    op.drop_table('a_contents')

    # Recreate the table with updated schema
    op.create_table(
        'a_contents',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('location_id', sa.String, sa.ForeignKey('locations.location_id'), nullable=False),
        sa.Column('pallet_id', sa.String(50), nullable=True),
        sa.Column('item_id', sa.String(50), sa.ForeignKey('items.item_id'), nullable=False),
        sa.Column('pieces_on_hand', sa.Integer, nullable=False, default=0),
        sa.Column('receipt_info', sa.String(100), nullable=True),
        sa.Column('receipt_release_num', sa.String(50), nullable=True),
        sa.Column('date_time_last_touched', sa.DateTime, nullable=False),
        sa.Column('user_last_touched', sa.String(50), nullable=False)
    )


def downgrade():
    # Recreate previous table (if needed)
    op.drop_table('a_contents')