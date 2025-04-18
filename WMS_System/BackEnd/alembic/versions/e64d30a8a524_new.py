"""New

Revision ID: e64d30a8a524
Revises: 35234e26d3a9
Create Date: 2025-04-10 14:36:05.300774

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e64d30a8a524'
down_revision: Union[str, None] = '35234e26d3a9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.execute("DROP TABLE IF EXISTS order_new")
    op.execute("DROP TABLE IF EXISTS order_new2")
    op.execute("DROP TABLE IF EXISTS order_new3")

def downgrade():
    pass  # no need to recreate them
