"""create order_lines tableV2

Revision ID: de7786c7538d
Revises: c5f855cb246f
Create Date: 2025-04-10 21:42:36.550949

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'de7786c7538d'
down_revision: Union[str, None] = 'c5f855cb246f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
