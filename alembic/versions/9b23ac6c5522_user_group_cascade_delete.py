"""user group cascade delete

Revision ID: 9b23ac6c5522
Revises: bfb5ee843884
Create Date: 2025-05-03 12:04:03.998532

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9b23ac6c5522'
down_revision: Union[str, None] = 'bfb5ee843884'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('user_group_membership_group_id_fkey', 'user_group_membership', type_='foreignkey')
    op.create_foreign_key(None, 'user_group_membership', 'user_groups', ['group_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'user_group_membership', type_='foreignkey')
    op.create_foreign_key('user_group_membership_group_id_fkey', 'user_group_membership', 'user_groups', ['group_id'], ['id'])
    # ### end Alembic commands ###
