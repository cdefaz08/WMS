"""Add is_taxable to items

Revision ID: 6b2b0a4d3717
Revises: 1710a7147208
Create Date: 2025-04-17 17:11:57.472042

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6b2b0a4d3717'
down_revision: Union[str, None] = '1710a7147208'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('items', sa.Column('is_taxable', sa.Boolean(), nullable=True))


def downgrade():
    op.drop_column('items', 'is_taxable')