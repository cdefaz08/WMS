"""add cubic feet columns to locations

Revision ID: f2158fd904d6
Revises: a19fa46f9200
Create Date: 2025-05-02 10:50:07.550876

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f2158fd904d6'
down_revision: Union[str, None] = 'a19fa46f9200'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Add new columns to locations
    op.add_column('locations', sa.Column('total_cubic_feet', sa.Float(), nullable=True))
    op.add_column('locations', sa.Column('used_cubic_feet', sa.Float(), nullable=True))


def downgrade():
    # Remove the columns if we downgrade
    op.drop_column('locations', 'used_cubic_feet')
    op.drop_column('locations', 'total_cubic_feet')