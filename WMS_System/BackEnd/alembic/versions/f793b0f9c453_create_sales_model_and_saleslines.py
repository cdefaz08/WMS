"""Create Sales model and SalesLines

Revision ID: f793b0f9c453
Revises: dd0750842186
Create Date: 2025-04-17 15:23:20.105512

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f793b0f9c453'
down_revision: Union[str, None] = 'dd0750842186'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
