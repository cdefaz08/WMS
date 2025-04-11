"""create order_lines table

Revision ID: c5f855cb246f
Revises: f83304bade6b
Create Date: 2025-04-10 21:41:43.135477

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c5f855cb246f'
down_revision: Union[str, None] = 'f83304bade6b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
