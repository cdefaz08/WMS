"""create pallets table

Revision ID: 5659a684a881
Revises: f2158fd904d6
Create Date: 2025-05-05 12:52:32.974715

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5659a684a881'
down_revision: Union[str, None] = 'f2158fd904d6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade():
    pass
def downgrade():
    pass