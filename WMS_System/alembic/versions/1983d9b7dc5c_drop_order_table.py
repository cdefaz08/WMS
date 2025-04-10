"""drop Order Table

Revision ID: 1983d9b7dc5c
Revises: e64d30a8a524
Create Date: 2025-04-10 15:00:56.439914

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1983d9b7dc5c'
down_revision: Union[str, None] = 'e64d30a8a524'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None



def upgrade():
    op.execute("DROP TABLE IF EXISTS orders")


def downgrade():
    pass  # no need to recreate them