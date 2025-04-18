"""Drop Purchase_orders table

Revision ID: 6ab052402a07
Revises: aaaf2cad04e4
Create Date: 2025-04-14 13:38:46.808199

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6ab052402a07'
down_revision: Union[str, None] = 'aaaf2cad04e4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.drop_table("purchase_orders")

    op.create_table(
        "purchase_orders",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("po_number", sa.String(50), nullable=False, unique=True),
        sa.Column("vendor_id", sa.Integer, nullable=False),
        sa.Column("order_date", sa.DateTime, nullable=False),
        sa.Column("expected_date", sa.DateTime),
        sa.Column("ship_date", sa.Date),
        sa.Column("status", sa.String(30), default="Open"),
        sa.Column("created_by", sa.String(50)),  # 👈 Nuevo: username como string
        sa.Column("created_date", sa.DateTime, server_default=sa.func.now()),
        sa.Column("modified_by", sa.String(50)),
        sa.Column("modified_date", sa.DateTime, onupdate=sa.func.now()),
        sa.Column("comments", sa.String(200)),
    )


def downgrade():
    op.drop_table("purchase_orders")