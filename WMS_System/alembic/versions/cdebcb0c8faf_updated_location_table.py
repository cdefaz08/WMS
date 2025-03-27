"""updated Location table

Revision ID: cdebcb0c8faf
Revises: 5e3f932382f5
Create Date: 2025-03-27 15:49:57.876064

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cdebcb0c8faf'
down_revision: Union[str, None] = '5e3f932382f5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
