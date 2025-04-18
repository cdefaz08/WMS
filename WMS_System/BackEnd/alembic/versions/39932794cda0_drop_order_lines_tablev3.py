"""drop order_lines tableV3

Revision ID: 39932794cda0
Revises: de7786c7538d
Create Date: 2025-04-10 21:43:21.901711

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '39932794cda0'
down_revision: Union[str, None] = 'de7786c7538d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.drop_table('order_lines')


def downgrade() -> None:
    """Downgrade schema."""
    pass
