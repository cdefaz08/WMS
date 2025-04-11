"""create order_lines tableV3

Revision ID: 8a5a74572bbd
Revises: 39932794cda0
Create Date: 2025-04-10 21:44:37.496681

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8a5a74572bbd'
down_revision: Union[str, None] = '39932794cda0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass

def downgrade() -> None:
    """Downgrade schema."""
    pass
