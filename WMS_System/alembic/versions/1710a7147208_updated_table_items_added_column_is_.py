"""Updated table items added column is_taxalbe

Revision ID: 1710a7147208
Revises: 182b7922a1b9
Create Date: 2025-04-17 17:10:33.697701

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1710a7147208'
down_revision: Union[str, None] = '182b7922a1b9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
