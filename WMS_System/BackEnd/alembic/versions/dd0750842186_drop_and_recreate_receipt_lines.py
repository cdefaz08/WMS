"""drop and recreate receipt_lines

Revision ID: dd0750842186
Revises: 4e9d92354ae0
Create Date: 2025-04-17 13:27:40.419413

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'dd0750842186'
down_revision: Union[str, None] = '4e9d92354ae0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
