"""Fase 1 of plan of implemetacion of tasks

Revision ID: f658f5cd728e
Revises: 6b2b0a4d3717
Create Date: 2025-04-18 12:47:01.856426

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f658f5cd728e'
down_revision: Union[str, None] = '6b2b0a4d3717'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
