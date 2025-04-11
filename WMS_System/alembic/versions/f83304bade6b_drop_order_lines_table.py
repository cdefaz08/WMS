"""drop order_lines table

Revision ID: f83304bade6b
Revises: 2b0c646e5fb7
Create Date: 2025-04-10 21:36:37.275692

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f83304bade6b'
down_revision: Union[str, None] = '2b0c646e5fb7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.drop_table('order_lines')


def downgrade():
    pass