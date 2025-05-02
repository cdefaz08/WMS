"""Updated the locations table to add max cube feet and used cubic feet

Revision ID: a19fa46f9200
Revises: a7b210788287
Create Date: 2025-05-02 10:47:51.402024

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a19fa46f9200'
down_revision: Union[str, None] = 'a7b210788287'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
