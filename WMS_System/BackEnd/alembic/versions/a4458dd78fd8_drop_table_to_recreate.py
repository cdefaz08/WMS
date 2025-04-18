"""Drop table to recreate

Revision ID: a4458dd78fd8
Revises: 6ab052402a07
Create Date: 2025-04-14 14:59:43.112170

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a4458dd78fd8'
down_revision: Union[str, None] = '6ab052402a07'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""



def downgrade() -> None:
    """Downgrade schema."""
