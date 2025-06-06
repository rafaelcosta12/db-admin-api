"""table columns

Revision ID: a6bddcdf0d40
Revises: 252f1806d9eb
Create Date: 2025-05-04 15:08:18.881548

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a6bddcdf0d40'
down_revision: Union[str, None] = '252f1806d9eb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('table_columns',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('table_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=128), nullable=False),
    sa.Column('type', sa.String(length=128), nullable=False),
    sa.Column('nullable', sa.Boolean(), nullable=False),
    sa.Column('default', sa.String(length=256), nullable=True),
    sa.Column('autoincrement', sa.Boolean(), nullable=False),
    sa.Column('comment', sa.String(length=256), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    sa.ForeignKeyConstraint(['table_id'], ['table_definitions.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('table_id', 'name', name='uq_table_columns')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('table_columns')
    # ### end Alembic commands ###
