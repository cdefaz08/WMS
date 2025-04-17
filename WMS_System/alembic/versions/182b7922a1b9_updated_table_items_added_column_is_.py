"""Updated table items added column is_taxalbe

Revision ID: 182b7922a1b9
Revises: f793b0f9c453
Create Date: 2025-04-17 17:08:11.903228

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '182b7922a1b9'
down_revision: Union[str, None] = 'f793b0f9c453'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
