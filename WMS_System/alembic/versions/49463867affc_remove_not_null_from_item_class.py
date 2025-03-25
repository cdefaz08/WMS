"""Remove NOT NULL from item_class

Revision ID: 49463867affc
Revises: 94258f425446
Create Date: 2025-03-25 13:23:25.640902

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '49463867affc'
down_revision: Union[str, None] = '94258f425446'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # 1. Crear una nueva tabla sin la restricción NOT NULL
    op.create_table(
        'items_new',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('item_id', sa.String(50), nullable=False),
        sa.Column('description', sa.String(60), nullable=False),
        sa.Column('price', sa.Float),
        sa.Column('upc', sa.Float, nullable=False),
        sa.Column('item_class', sa.String(50), nullable=True),  # ✅ NOT NULL eliminado
        sa.Column('is_offer', sa.Boolean),
        sa.Column('default_cfg', sa.String(10)),
        sa.Column('custum1', sa.String(30)),
        sa.Column('custum2', sa.String(30)),
        sa.Column('custum3', sa.String(30)),
        sa.Column('custum4', sa.String(30)),
        sa.Column('custum5', sa.String(30)),
        sa.Column('custum6', sa.String(30)),
    )

    # 2. Copiar los datos de la tabla antigua a la nueva
    op.execute("""
        INSERT INTO items_new (
            id, item_id, description, price, upc, item_class, is_offer, default_cfg,
            custum1, custum2, custum3, custum4, custum5, custum6
        )
        SELECT
            id, item_id, description, price, upc, item_class, is_offer, default_cfg,
            custum1, custum2, custum3, custum4, custum5, custum6
        FROM items
    """)

    # 3. Eliminar la tabla antigua
    op.drop_table('items')

    # 4. Renombrar la tabla nueva como la tabla original
    op.rename_table('items_new', 'items')

def downgrade():
    pass  # Opcional si no deseas implementar una reversión