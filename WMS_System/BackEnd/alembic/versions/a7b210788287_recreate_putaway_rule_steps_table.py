"""Recreate putaway_rule_steps table

Revision ID: a7b210788287
Revises: f658f5cd728e
Create Date: 2025-04-21 17:16:56.336896

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a7b210788287'
down_revision: Union[str, None] = 'f658f5cd728e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Drop the old table if it exists
    op.drop_table('putaway_rule_steps')

    # Create new table with updated schema
    op.create_table(
        'putaway_rule_steps',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('rule_id', sa.Integer(), sa.ForeignKey('putaway_rules.id')),
        sa.Column('seq', sa.Integer()),
        sa.Column('min_percent', sa.Float()),
        sa.Column('max_percent', sa.Float()),
        sa.Column('UOM', sa.String()),
        sa.Column('location_type_from', sa.String()),
        sa.Column('putaway_to', sa.String()),
        sa.Column('location_type_to', sa.String()),
        sa.Column('putaway_group', sa.String()),
        sa.Column('sort_expresion', sa.String()),
        sa.Column('max_loc_check', sa.Integer())
    )


def downgrade():
    # Drop the new table
    op.drop_table('putaway_rule_steps')

    # (Optional) You can recreate the old version of the table here if needed