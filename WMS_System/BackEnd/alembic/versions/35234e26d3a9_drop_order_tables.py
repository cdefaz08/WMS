"""Drop order tables

Revision ID: 35234e26d3a9
Revises: ae8b445b3302
Create Date: 2025-04-10 14:34:25.963192

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '35234e26d3a9'
down_revision: Union[str, None] = 'ae8b445b3302'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


from alembic import op

def upgrade():
    op.execute("DROP TABLE IF EXISTS order_new")
    op.execute("DROP TABLE IF EXISTS order_new2")
    op.execute("DROP TABLE IF EXISTS order_new3")

def downgrade():
    pass  # no need to recreate them
